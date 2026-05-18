from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'full_name', 'phone', 'company_name')
    list_filter = ('role', 'field', 'sector')
    search_fields = ('user__username', 'full_name', 'company_name', 'phone')
