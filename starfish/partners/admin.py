from django.contrib import admin

from starfish.admin import SoftDeletableAdminMixin

from .models import Affiliate, PartnerCampaign, Pledge


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


class PledgeInline(admin.TabularInline):
    model = Pledge
    extra = 1
    readonly_fields = ('created',)


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('organization_name',)
    search_fields = ('organization_name', 'notes')
    inlines = [PledgeInline]
