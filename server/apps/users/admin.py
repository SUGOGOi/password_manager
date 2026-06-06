from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import User, EmailOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ["email", "username", "is_email_verified", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "is_email_verified"]
    search_fields = ["email", "username"]
    ordering = ["email"]
    readonly_fields = ["last_login", "date_joined"]

    fieldsets = [
        ("Login Info", {"fields": ["email", "username", "password"]}),
        ("Personal Info", {"fields": ["first_name", "last_name"]}),
        ("Verification", {"fields": ["is_email_verified"]}),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Important Dates",
            {"fields": ["last_login", "date_joined"], "classes": ["collapse"]},
        ),
    ]


@admin.register(EmailOTP)
class EmailOTPAdmin(ModelAdmin):
    list_display = ["user", "otp", "is_used", "created_at", "is_valid_display"]
    list_filter = ["is_used"]
    search_fields = ["user__email", "otp"]
    ordering = ["-created_at"]
    readonly_fields = ["user", "otp", "created_at"]

    @admin.display(description="Valid", boolean=True)
    def is_valid_display(self, obj):
        return obj.is_valid()
