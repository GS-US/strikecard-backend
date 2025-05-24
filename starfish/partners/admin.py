from django.contrib import admin
from django.db.models import Sum
from unfold.admin import ModelAdmin, TabularInline

from starfish.admin import SoftDeletableAdminMixin

from .models import Affiliate, PartnerCampaign, Pledge


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(SoftDeletableAdminMixin, ModelAdmin):
    list_display = (
        'name',
        'email',
        'url',
        'last_used',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified')
    readonly_fields = ('key_string', 'created', 'modified', 'last_used')
    compressed_fields = True


class PledgeInline(TabularInline):
    model = Pledge
    extra = 1
    readonly_fields = (
        'created',
        'submitted_by_user',
    )


@admin.register(Affiliate)
class AffiliateAdmin(SoftDeletableAdminMixin, ModelAdmin):
    list_display = ('organization_name', 'total_pledged')
    search_fields = ('organization_name', 'email', 'notes')
    readonly_fields = ('created', 'modified')
    inlines = [PledgeInline]
    compressed_fields = True

    def total_pledged(self, obj):
        total = obj.pledges.aggregate(total=Sum('count'))['total']
        return total or 0
        instances = formset.save(commit=False)
        for obj in instances:
            if isinstance(obj, Pledge) and not obj.submitted_by_user_id:
                obj.submitted_by_user = request.user
            obj.save()
        formset.save_m2m()
