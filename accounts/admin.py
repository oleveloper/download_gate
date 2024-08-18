# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active', 'is_pending']
    list_filter = ['is_staff', 'is_active', 'is_pending']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'profile_image')}),
        ('Permissions',
         {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_pending', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('date_joined',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'profile_image', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets = [
                (name, {'fields': [f for f in data['fields'] if f not in ('is_staff', 'is_superuser')]})
                for name, data in fieldsets
            ]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields += ('is_staff', 'is_superuser')
        return readonly_fields


admin.site.register(CustomUser, CustomUserAdmin)
