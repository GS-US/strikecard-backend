import rules
from chapters.models import ChapterRole
from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from import_export.admin import ImportExportMixin
from members.models import Member, MemberNote
from members.resources import MemberResource
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in ('chapter', 'partner_campaign'):
            if f in self.fields:
                widget = self.fields[f].widget
                widget.can_add_related = False
                widget.can_change_related = False
                widget.can_delete_related = False


class MemberNoteInlineFormSet(BaseInlineFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['note'].widget.attrs['rows'] = 3
        if form.instance.pk:
            form.fields['note'].disabled = True
            form.fields['note'].required = False


class MemberNoteInlineForm(forms.ModelForm):
    class Meta:
        model = MemberNote
        fields = ('note',)


class MemberNoteInline(admin.TabularInline):
    model = MemberNote
    form = MemberNoteInlineForm
    formset = MemberNoteInlineFormSet
    fields = ('note', 'created_by', 'created')
    readonly_fields = ('created_by', 'created')
    extra = 1
    can_delete = False
    tab = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by')


@admin.register(Member)
class MemberAdmin(
    ImportExportMixin,
    ObjectPermissionsModelAdmin,
    SimpleHistoryAdmin,
    ModelAdmin,
):
    resource_class = MemberResource
    list_display = (
        'name',
        'email',
        'chapter',
        'leadership_score',
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
    form = MemberForm
    compressed_fields = True
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = [MemberNoteInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if isinstance(obj, MemberNote) and not obj.created_by_id:
                obj.created_by = request.user
            obj.save()
        formset.save_m2m()

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('members.view_member', request.user, obj)
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('members.change_member', request.user, obj)
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return rules.test_perm('members.add_member', request.user)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        user_chapters = ChapterRole.objects.filter(user=request.user).values_list(
            'chapter', flat=True
        )
        return qs.filter(chapter__in=user_chapters)
