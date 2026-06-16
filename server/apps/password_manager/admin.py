from django.contrib import admin
from .models import Password


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created_at"]
    list_display_links = ["name"]
    list_filter = ["created_at"]
    search_fields = ["name", "username"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_per_page = 20
    date_hierarchy = "created_at"

    fieldsets = [
        ("Password Info", {"fields": ["name", "username", "password"]}),
        ("Ownership", {"fields": ["user"]}),
        (
            "Timestamps",
            {"fields": ["created_at", "updated_````at"], "classes": ["collapse"]},
        ),
    ]
