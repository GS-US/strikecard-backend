import rules
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterZip,
    PaperTotal,
)


class ChapterZipInline(admin.TabularInline):
    model = ChapterZip
    autocomplete_fields = ['zip_code']
    extra = 1


class ChapterRoleInline(admin.TabularInline):
    model = ChapterRole
    readonly_fields = ['added_by_user']
    extra = 1


class ChapterSocialLinkInline(admin.TabularInline):
    model = ChapterSocialLink
    extra = 1


class PaperTotalInline(admin.TabularInline):
    model = PaperTotal
    readonly_fields = ['submitted_by_user']
    extra = 1


@admin.register(Chapter)
class ChapterAdmin(ObjectPermissionsModelAdmin):
    list_display = ('title', 'created')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['states']

    inlines = [
        ChapterRoleInline,
        ChapterSocialLinkInline,
        PaperTotalInline,
        ChapterZipInline,
    ]

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
class ChapterZipAdmin(admin.ModelAdmin):
    list_display = ['zip_code', 'chapter', 'state']
    autocomplete_fields = ['chapter', 'zip_code']
    list_filter = ['chapter']
    fields = ['chapter', 'zip_code']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields]
        else:
            return []
