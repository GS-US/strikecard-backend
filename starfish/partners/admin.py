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
    inlines = [PledgeInline]


class PledgeInline(admin.TabularInline):
    model = Pledge
    extra = 0  # Number of empty forms to display
    readonly_fields = ('created',)
