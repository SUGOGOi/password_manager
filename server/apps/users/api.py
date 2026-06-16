from ninja import Router
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail
from .schemas import (
    LoginIn,
    RegisterIn,
    UserOut,
    VerifyOTPIn,
    ResendOTPIn,
    ForgotPasswordIn,
    ResetPasswordIn,
)
from .models import User, EmailOTP, generate_otp
from .auth import CookieAuth
import json
from .utils import create_access_token
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount
from .csrf import get_csrf_token

router = Router(tags=["Auth"])


@router.post("/register")
def register(request: HttpRequest, payload: RegisterIn):
    if User.objects.filter(email=payload.email).exists():
        return HttpResponse(
            json.dumps({"message": "Email already registered"}),
            content_type="application/json",
            status=400,
        )

    # create user but don't allow login yet
    user = User.objects.create_user(
        email=payload.email,
        username=payload.username,
        password=payload.password,
        is_email_verified=False,
    )

    # delete any existing OTPs
    EmailOTP.objects.filter(user=user).delete()

    # generate and send OTP
    otp_code = generate_otp()
    EmailOTP.objects.create(user=user, otp=otp_code)

    send_mail(
        subject="Verify your email",
        message=f"Your OTP is: {otp_code}\n\nThis OTP expires in 10 minutes.",
        from_email="noreply@todoapp.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return HttpResponse(
        json.dumps(
            {
                "message": "Registration successful. Please check your email for OTP.",
                "email": user.email,
            }
        ),
        content_type="application/json",
        status=201,
    )


@router.post("/verify-otp", response={200: dict, 400: dict})
def verify_otp(request: HttpRequest, payload: VerifyOTPIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return 400, {"message": "User not found"}

    # get latest unused OTP
    otp = EmailOTP.objects.filter(user=user, otp=payload.otp, is_used=False).last()

    if not otp or not otp.is_valid():
        return 400, {"message": "Invalid or expired OTP"}

    # mark OTP as used and verify email
    otp.is_used = True
    otp.save()

    user.is_email_verified = True
    user.save()

    return 200, {"message": "Email verified successfully. You can now login."}


@router.post("/login")
def user_login(request: HttpRequest, payload: LoginIn):
    user = authenticate(request, email=payload.email, password=payload.password)
    if user is None:
        return HttpResponse(
            json.dumps({"message": "Invalid email or password"}),
            content_type="application/json",
            status=401,
        )

    # block login if email not verified
    if not getattr(user, "is_email_verified", False):
        return HttpResponse(
            json.dumps(
                {
                    "message": "Email not verified. Please verify your email first.",
                    "email": getattr(user, "email", ""),
                }
            ),
            content_type="application/json",
            status=403,
        )

    from .utils import create_access_token

    token = create_access_token(user)

    response = HttpResponse(
        json.dumps(
            {
                "pk": user.pk,
                "email": getattr(user, "email", ""),
                "username": getattr(user, "username", ""),
            }
        ),
        content_type="application/json",
        status=200,
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60,
    )
    return response


@router.post("/resend-otp", response={200: dict, 400: dict})
def resend_otp(request: HttpRequest, payload: ResendOTPIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return 400, {"message": "User not found"}

    if user.is_email_verified:
        return 400, {"message": "Email already verified"}

    # delete all previous OTPs for this user
    EmailOTP.objects.filter(user=user).delete()

    otp_code = generate_otp()
    EmailOTP.objects.create(user=user, otp=otp_code)

    send_mail(
        subject="Verify your email - New OTP",
        message=f"Your new OTP is: {otp_code}\n\nThis OTP expires in 10 minutes.",
        from_email="noreply@todoapp.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return 200, {"message": "New OTP sent to your email"}


@router.post("/logout")
def user_logout(request: HttpRequest):
    response = HttpResponse(
        json.dumps({"message": "Logged out successfully"}),
        content_type="application/json",
        status=200,
    )
    response.delete_cookie(
        key="access_token",
        path="/",
    )

    return response


@router.get("/me", auth=CookieAuth(), response={200: UserOut})
def me(request: HttpRequest):
    user = getattr(request, "auth")
    social = SocialAccount.objects.filter(user=user, provider="google").first()
    profile_photo = social.extra_data.get("picture") if social else None

    return 200, {
        "pk": user.pk,
        "email": user.email,
        "username": user.username,
        "is_email_verified": user.is_email_verified,
        "is_oauth_user": SocialAccount.objects.filter(user=user).exists(),
        "profile_photo": profile_photo,
    }


@router.get("/google/callback")
def google_callback(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponse(
            json.dumps({"message": "Google auth failed"}),
            content_type="application/json",
            status=401,
        )

    # auto verify email for Google users
    user = User.objects.get(pk=request.user.pk)
    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()

    token = create_access_token(request.user)
    response = redirect("http://localhost:3000")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60,
    )
    return response


@router.post("/forgot-password", response={200: dict, 400: dict})
def forgot_password(request: HttpRequest, payload: ForgotPasswordIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return 400, {"message": "User does not exist"}

    # Single optimized query
    social_account = SocialAccount.objects.filter(user=user).first()
    if social_account:
        provider = social_account.provider
        return 400, {
            "message": f"This account uses {provider} login. Please sign in with {provider} instead."
        }

    # delete old otps and create new one
    EmailOTP.objects.filter(user=user).delete()
    otp_code = generate_otp()
    EmailOTP.objects.create(user=user, otp=otp_code)

    send_mail(
        subject="Reset your password",
        message=f"Your password reset OTP is: {otp_code}\n\nThis OTP expires in 10 minutes.",
        from_email="noreply@todoapp.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return 200, {"message": "OTP has been sent"}


@router.post("/reset-password", response={200: dict, 400: dict})
def reset_password(request: HttpRequest, payload: ResetPasswordIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return 400, {"message": "User not found"}

    otp = EmailOTP.objects.filter(user=user, otp=payload.otp, is_used=False).last()

    if not otp or not otp.is_valid():
        return 400, {"message": "Invalid or expired OTP"}

    otp.is_used = True
    otp.save()

    user.set_password(payload.new_password)
    user.save()

    return 200, {"message": "Password reset successfully"}


@router.get("/csrf", auth=None)
def csrf_token_view(request):
    return get_csrf_token(request)
