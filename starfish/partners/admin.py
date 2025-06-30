from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline

from starfish.admin import SoftDeletableAdminMixin, pretty_button

from .models import Affiliate, PartnerCampaign, Pledge


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(SoftDeletableAdminMixin, SimpleHistoryAdmin, ModelAdmin):
    list_display = (
        'name',
        'email',
        'url',
        'members',
        'last_used',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified')
    prepopulated_fields = {'slug': ['name']}
    readonly_fields = (
        'created',
        'modified',
        'last_used',
        'view_members_link',
    )
    compressed_fields = True

    def members(self, obj):
        return obj.members.count() or 0

    def view_members_link(self, obj):
        return pretty_button(
            reverse('admin:members_member_changelist')
            + f'?partner_campaign__id__exact={obj.id}',
            'View members',
        )

    view_members_link.short_description = 'Members'


class PledgeInline(TabularInline):
    model = Pledge
    extra = 1
    readonly_fields = (
        'created',
        'submitted_by_user',
    )


@admin.register(Affiliate)
class AffiliateAdmin(SoftDeletableAdminMixin, SimpleHistoryAdmin, ModelAdmin):
    list_display = ('organization_name', 'total_pledged')
    search_fields = ('organization_name', 'contact_email', 'notes')
    readonly_fields = ('created', 'modified')
    inlines = [PledgeInline]
    compressed_fields = True

    def total_pledged(self, obj):
        return obj.pledges.aggregate(total=Sum('count'))['total'] or 0

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if isinstance(obj, Pledge) and not obj.submitted_by_user_id:
                obj.submitted_by_user = request.user
            obj.save()
        formset.save_m2m()
