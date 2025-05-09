from django.contrib import admin

from starfish.admin import SoftDeletableAdminMixin

from .models import Affiliate, Pledge, PartnerCampaign


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(SoftDeletableAdminMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'url',
        'last_used_at',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified')
    readonly_fields = ('key_string', 'created', 'modified', 'last_used_at')


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('organization_name',)
    search_fields = ('organization_name', 'notes')


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'count', 'submitted_by_user', 'created')
    list_filter = ('created', 'affiliate')
    search_fields = (
        'affiliate__organization_name',
        'notes',
        'submitted_by_user__username',
    )
    readonly_fields = ('created',)
