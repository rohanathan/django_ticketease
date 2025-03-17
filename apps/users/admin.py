# apps/users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Fields to show in the user list
    list_display = (
        "username",
        "email",
        "phone_number",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    
    # Fields to show when editing a user
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",  # Section heading
            {
                "fields": (
                    "profile_picture",
                    "phone_number",
                    "date_of_birth",
                )
            },
        ),
    )
    
    # Fields to show when creating a user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "date_of_birth",
                    "profile_picture",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
