from ninja import Schema
from pydantic import EmailStr


class RegisterIn(Schema):
    email: EmailStr
    username: str
    password: str


class LoginIn(Schema):
    email: EmailStr
    password: str


class UserOut(Schema):
    pk: int
    email: str
    username: str
    is_email_verified: bool
    is_oauth_user: bool
    profile_photo: str | None  # ← add this


class TokenOut(Schema):
    token: str
    user: UserOut


class VerifyOTPIn(Schema):
    email: EmailStr
    otp: str


class ResendOTPIn(Schema):
    email: EmailStr


class ForgotPasswordIn(Schema):
    email: EmailStr


class ResetPasswordIn(Schema):
    email: EmailStr
    otp: str
    new_password: str
