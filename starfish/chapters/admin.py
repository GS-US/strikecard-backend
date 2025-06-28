import rules
from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterZip,
    OfflineTotal,
)
from django.contrib import admin
from django.urls import reverse
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter

from starfish.admin import SoftDeletableAdminMixin, pretty_button


class ChapterZipInline(TabularInline):
    model = ChapterZip
    fields = ['zip_code', 'county']
    autocomplete_fields = ['zip_code']
    extra = 1
    tab = True
    verbose_name = 'ZIP'
    readonly_fields = ['county']

    def county(self, obj):
        return obj.zip_code.county


class ChapterRoleInline(TabularInline):
    model = ChapterRole
    readonly_fields = ['added_by_user']
    autocomplete_fields = ['user']
    extra = 1
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
    autocomplete_fields = ['nearby_chapters']
    readonly_fields = ('view_contacts_link',)
    compressed_fields = True
    fields = (
        'state',
        'title',
        'slug',
        'nearby_chapters',
        'view_contacts_link',
        'description',
        'contact_email',
        'website_url',
    )

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
            f'View {obj.total_contacts} contacts',
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
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()


@admin.register(ChapterZip)
class ChapterZipAdmin(ModelAdmin):
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
