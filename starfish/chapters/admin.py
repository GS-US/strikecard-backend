import rules
from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterZip,
    OfflineTotal,
)
from django import forms
from django.contrib import admin
from django.urls import reverse
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter

from starfish.admin import SoftDeletableAdminMixin, pretty_button


class ChapterZipForm(forms.ModelForm):
    class Meta:
        model = ChapterZip
        fields = '__all__'

    def clean_zip_code(self):
        if "state" in self.data:
            state = self.data["state"]
        elif "chapter" in self.cleaned_data:
            state = self.cleaned_data["chapter"].state.code
        zip_code = self.cleaned_data["zip_code"]
        if zip_code.state.code != state:
            raise forms.ValidationError(
                "Zip code must be in the same state as the chapter"
            )
        return zip_code


class ChapterZipInline(TabularInline):
    model = ChapterZip
    form = ChapterZipForm
    fields = ['zip_code', 'county']
    autocomplete_fields = ['zip_code']
    extra = 1
    tab = True
    verbose_name = 'ZIP'
    readonly_fields = ['county']

    def county(self, obj):
        return obj.zip_code.county


class ChapterRoleInlineForm(forms.ModelForm):

    class Meta:
        model = ChapterRole
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'user' in self.fields:
            widget = self.fields['user'].widget
            widget.can_add_related = False
            widget.can_change_related = False
            widget.can_delete_related = False


class ChapterRoleInline(TabularInline):
    model = ChapterRole
    readonly_fields = ['added_by_user']
    autocomplete_fields = ['user']
    extra = 1
    form = ChapterRoleInlineForm
    tab = True
    verbose_name = 'Role'


class ChapterSocialLinkInline(TabularInline):
    model = ChapterSocialLink
    extra = 1
    tab = True
    verbose_name = 'Link'


class OfflineTotalInline(TabularInline):
    model = OfflineTotal
    readonly_fields = ['submitted_by_user']
    extra = 1
    tab = True


@admin.register(Chapter)
class ChapterAdmin(
    SoftDeletableAdminMixin, ObjectPermissionsModelAdmin, SimpleHistoryAdmin, ModelAdmin
):
    list_display = ('title', 'total_contacts', 'created')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['state', 'nearby_chapters']
    readonly_fields = ('view_contacts_link',)
    compressed_fields = True

    inlines = [
        ChapterRoleInline,
        ChapterSocialLinkInline,
        OfflineTotalInline,
        ChapterZipInline,
    ]

    def view_contacts_link(self, obj):
        return pretty_button(
            reverse('admin:contacts_contact_changelist')
            + f'?chapter_id__exact={obj.id}',
            'View contacts',
        )

    view_contacts_link.short_description = 'Contacts'

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('chapters.view_chapter', request.user, obj)
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('chapters.change_chapter', request.user, obj)
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_chapters = ChapterRole.objects.filter(user=request.user).values_list(
            'chapter', flat=True
        )
        return qs.filter(id__in=user_chapters)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if isinstance(obj, OfflineTotal) and not obj.submitted_by_user_id:
                obj.submitted_by_user = request.user
            if isinstance(obj, ChapterRole) and not obj.added_by_user_id:
                obj.added_by_user = request.user
            obj.save()
        formset.save_m2m()


@admin.register(ChapterZip)
class ChapterZipAdmin(ModelAdmin):
    form = ChapterZipForm
    list_display = [
        'zip_code',
        'chapter',
    ]
    search_fields = [
        'zip_code__code',
        'chapter__title',
    ]
    autocomplete_fields = ['chapter', 'zip_code']
    list_filter = [
        ('chapter', AutocompleteSelectMultipleFilter),
    ]
    fields = ['chapter', 'zip_code']
    compressed_fields = True
    list_filter_submit = True

    def state(self, obj):
        return obj.chapter.state

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields]
        else:
            return []
