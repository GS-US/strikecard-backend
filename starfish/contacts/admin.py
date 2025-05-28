import rules
from django import forms
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    AutocompleteSelectMultipleFilter,
)

from chapters.models import ChapterRole
from contacts.models import Contact

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'chapter__title',
            'partner_campaign__name',
            'validated',
        )
        export_order = (
            'id',
            'name',
            'email',
            'phone',
            'chapter__title',
            'partner_campaign__name',
            'validated',
        )


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
class ContactAdmin(
    ImportExportModelAdmin,
    ObjectPermissionsModelAdmin,
    SimpleHistoryAdmin,
    ModelAdmin,
):
    resource_class = ContactResource
    list_display = (
        'name',
        'email',
        'chapter',
        'partner_campaign',
        'validated',
    )
    search_fields = ('name', 'email')
    list_display_links = ('name', 'email')
    list_filter = (('chapter', AutocompleteSelectMultipleFilter), 'validated')
    list_filter_submit = True
    autocomplete_fields = ['zip_code']
    readonly_fields = ['referer_full', 'validated']
    exclude = ['referer_host']
    date_hierarchy = 'validated'
    form = ContactForm
    compressed_fields = True

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
