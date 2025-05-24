import csv

import rules
from django import forms
from django.contrib import admin
from django.http import HttpResponse
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminTextInputWidget

from chapters.models import ChapterRole
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in ('chapter', 'partner_campaign'):
            if f in self.fields:
                widget = self.fields[f].widget
                widget.can_add_related = False
                widget.can_change_related = False
                widget.can_delete_related = False


@admin.register(Contact)
class ContactAdmin(ObjectPermissionsModelAdmin, SimpleHistoryAdmin, ModelAdmin):
    list_display = (
        'name',
        'email',
        'chapter',
        'partner_campaign',
        'validated',
    )
    search_fields = ('name', 'email')
    list_filter = ('validated', 'chapter')
    autocomplete_fields = ['zip_code']
    readonly_fields = ['referer_full', 'validated']
    exclude = ['referer_host']
    date_hierarchy = 'validated'
    actions = ['export_as_csv']
    form = ContactForm
    compressed_fields = True

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=contacts.csv'
        writer = csv.writer(response)
        writer.writerow(
            [
                'Name',
                'Email',
                'Phone',
                'Chapter',
                'Partner Campaign',
                'Validated Date',
            ]
        )
        for obj in queryset:
            writer.writerow(
                [
                    obj.name,
                    obj.email,
                    obj.phone,
                    obj.chapter.title if obj.chapter else '',
                    obj.partner_campaign.name if obj.partner_campaign else '',
                    (
                        obj.validated.strftime('%Y-%m-%d %H:%M:%S')
                        if obj.validated
                        else ''
                    ),
                ]
            )
        return response

    export_as_csv.short_description = 'Export selected contacts as CSV'

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('contacts.view_contact', request.user, obj)
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('contacts.change_contact', request.user, obj)
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return rules.test_perm('contacts.add_contact', request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('contacts.delete_contact', request.user, obj)
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        user_chapters = ChapterRole.objects.filter(user=request.user).values_list(
            'chapter', flat=True
        )
        return qs.filter(chapter__in=user_chapters)
