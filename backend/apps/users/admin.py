from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'investor_profile', 'is_staff')
    list_filter = ('investor_profile', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil de Investimento', {'fields': ('investor_profile',)}),
    )
