from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account


class AccountAdmin(UserAdmin):
    list_display = [
        "id",
        "email",
        "name",
        "terms",
        "date_of_birth",
        "is_active",
        "is_admin",
        "created",
        "updated",
    ]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "terms", "date_of_birth"]}),
        ("Permissions", {"fields": ["is_active", "is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "terms", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["id", "email", "name"]
    filter_horizontal = []


admin.site.register(Account, AccountAdmin)
