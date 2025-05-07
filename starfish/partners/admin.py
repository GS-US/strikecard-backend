from django.contrib import admin

from .models import PartnerCampaign


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'url', 'last_used_at', 'is_removed')
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified', 'is_removed')
    readonly_fields = ('key_string', 'created', 'modified', 'last_used_at')
