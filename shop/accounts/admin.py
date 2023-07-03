from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_staff',)
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login', 'username',)

    filter_horizontal = ()
    list_filter = ()

    add_fieldsets = (
        ('Login info', {'fields': ('email', 'password1', 'password2',)}),
    )

    fieldsets = (
        ('Login info', {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'username', 'observed_cars', 'observed_parts', 'observed_motorcycles',)}),
    )

admin.site.register(Account, AccountAdmin)