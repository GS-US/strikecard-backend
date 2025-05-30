import rules
from django import forms
from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html
from rules.contrib.admin import ObjectPermissionsModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline

from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterZip,
    PaperTotal,
)
from starfish.admin import SoftDeletableAdminMixin


class ChapterZipInline(TabularInline):
    model = ChapterZip
    autocomplete_fields = ['zip_code']
    extra = 1
    tab = True
    verbose_name = 'ZIP'


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


class PaperTotalInline(TabularInline):
    model = PaperTotal
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
    autocomplete_fields = ['states']
    readonly_fields = ('view_contacts_link',)
    compressed_fields = True

    inlines = [
        ChapterRoleInline,
        ChapterSocialLinkInline,
        PaperTotalInline,
        ChapterZipInline,
    ]

    def view_contacts_link(self, obj):
        url = reverse('admin:contacts_contact_changelist')
        url += f'?chapter_id__exact={obj.id}'
        return format_html(
            '<a class="inline-block bg-primary-600 text-white font-semibold py-1 px-3 rounded text-sm no-underline" href="{}">View contacts</a>',
            url,
        )

    view_contacts_link.short_description = 'Contacts'

    def total_contacts(self, obj):
        contacts_count = obj.contacts.count()
        expunged_contacts_count = obj.expunged_contacts.count()
        paper_total_count = obj.paper_totals.aggregate(Sum('count'))['count__sum'] or 0
        return contacts_count + expunged_contacts_count + paper_total_count

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
            if isinstance(obj, PaperTotal) and not obj.submitted_by_user_id:
                obj.submitted_by_user = request.user
            obj.save()
        formset.save_m2m()


@admin.register(ChapterZip)
class ChapterZipAdmin(ModelAdmin):
    list_display = ['zip_code', 'chapter', 'state']
    search_fields = ['zip_code__code']
    autocomplete_fields = ['chapter', 'zip_code']
    list_filter = [
        'chapter',
    ]
    fields = ['chapter', 'zip_code']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields]
        else:
            return []
