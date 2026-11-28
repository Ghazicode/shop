from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """

    model = User
    list_display = ("id", "email", "is_superuser", "is_active", )
    list_filter = ("email", "is_superuser", "is_active", )
    searching_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions", "type"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "type",
                ),
            },
        ),
    )


class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "fullname", "phone_number")
    searching_fields = ("user", "fullname", "phone_number")


admin.site.register(models.Profile, CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)

from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]


admin.site.register(Session, SessionAdmin)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("fullname", "message", "email", "subject")


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "fullname",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "user__email",
        "fullname",
        "phone_number",
        "postal_code",
        "title",
    )

    list_per_page = 25
