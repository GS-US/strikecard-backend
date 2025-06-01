from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html
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
        'contacts',
        'last_used',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified')
    readonly_fields = (
        'slug',
        'created',
        'modified',
        'last_used',
        'view_contacts_link',
    )
    compressed_fields = True

    def contacts(self, obj):
        return obj.contacts.count() or 0

    def view_contacts_link(self, obj):
        return pretty_button(
            reverse('admin:contacts_contact_changelist')
            + f'?partner_campaign__id__exact={obj.id}',
            'View contacts',
        )

    view_contacts_link.short_description = 'Contacts'


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
