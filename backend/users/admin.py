from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'role', 'department', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Infos Métier', {'fields': ('role', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Infos Métier', {'fields': ('role', 'department')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)