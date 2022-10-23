from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreateForm
from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    add_form = AccountCreateForm
    list_display = ['first_name', 'last_name', 'email']
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2",)
            }
        ),
    )
