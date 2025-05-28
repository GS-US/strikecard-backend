from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline

from starfish.admin import SoftDeletableAdminMixin

from .models import Affiliate, PartnerCampaign, Pledge


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(SoftDeletableAdminMixin, SimpleHistoryAdmin, ModelAdmin):
    list_display = (
        'name',
        'email',
        'url',
        'last_used',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified')
    readonly_fields = (
        'key_string',
        'created',
        'modified',
        'last_used',
        'view_contacts_link',
    )
    compressed_fields = True

    def view_contacts_link(self, obj):
        url = reverse('admin:contacts_contact_changelist')
        url += f'?partner_campaign__id__exact={obj.id}'
        return format_html('<a href="{}">View contacts</a>', url)

    view_contacts_link.short_description = 'Related Contacts'


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
    search_fields = ('organization_name', 'email', 'notes')
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
