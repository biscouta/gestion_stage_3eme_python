from django.contrib import admin

from .models import InternshipOffer


@admin.register(InternshipOffer)
class InternshipOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'domain', 'internship_type', 'deadline', 'status', 'created_at')
    list_filter = ('status', 'internship_type', 'domain')
    search_fields = ('title', 'company__username', 'domain', 'location')
