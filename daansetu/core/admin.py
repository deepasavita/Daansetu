from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ItemDonation, MoneyDonation, VolunteerAssignment

class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin configuration
    """
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active',)
    list_filter = ('role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)


class ItemDonationAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'donor', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item_name', 'description', 'donor__username')


class MoneyDonationAdmin(admin.ModelAdmin):
    list_display = ('amount', 'donor', 'date')
    list_filter = ('date',)
    search_fields = ('donor__username',)


class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'item', 'status', 'assigned_at', 'completed_at')
    list_filter = ('status', 'assigned_at', 'completed_at')
    search_fields = ('volunteer__username', 'item__item_name')


# Register your models with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(ItemDonation, ItemDonationAdmin)
admin.site.register(MoneyDonation, MoneyDonationAdmin)
admin.site.register(VolunteerAssignment, VolunteerAssignmentAdmin)
