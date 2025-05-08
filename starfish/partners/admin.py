from django.contrib import admin

from starfish.admin import SoftDeletableAdmin

from .models import PartnerCampaign


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(SoftDeletableAdmin):
    list_display = (
        'name',
        'email',
        'url',
        'last_used_at',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified')
    readonly_fields = ('key_string', 'created', 'modified', 'last_used_at')
