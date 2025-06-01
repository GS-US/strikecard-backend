import rules
from django import forms
from django.contrib import admin
from import_export.admin import ImportExportMixin
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from chapters.models import ChapterRole
from contacts.models import Contact, ContactNote
from contacts.resources import ContactResource


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


class ContactNoteInline(admin.TabularInline):
    model = ContactNote
    fields = ('note', 'created_by', 'created')
    readonly_fields = ('created_by', 'created')
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return True

    def save_new_object(self, form, commit=True):
        obj = form.save(commit=False)
        obj.created_by = form.request.user
        if commit:
            obj.save()
        return obj

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


@admin.register(Contact)
class ContactAdmin(
    ImportExportMixin,
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
    list_filter = (
        ('chapter', AutocompleteSelectMultipleFilter),
        ('partner_campaign', AutocompleteSelectMultipleFilter),
        'validated',
    )
    list_filter_submit = True
    autocomplete_fields = ['zip_code', 'chapter', 'partner_campaign']
    readonly_fields = ['referer_full', 'validated']
    exclude = ['referer_host']
    date_hierarchy = 'validated'
    form = ContactForm
    compressed_fields = True
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = [ContactNoteInline]

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


@admin.register(ContactNote)
class ContactNoteAdmin(admin.ModelAdmin):
    list_display = ('contact', 'created_by', 'created')
    fields = ('contact', 'note', 'created_by', 'created')
    readonly_fields = ('created_by', 'created')
    date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        # Prevent editing of existing notes
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of notes
        return False
