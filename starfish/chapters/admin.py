import rules
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterState,
    ChapterZip,
    PaperTotal,
)


class ChapterZipInline(admin.TabularInline):
    model = ChapterZip
    extra = 1


class ChapterStateInline(admin.TabularInline):
    model = ChapterState
    extra = 1


class ChapterRoleInline(admin.TabularInline):
    model = ChapterRole
    extra = 1


class ChapterSocialLinkInline(admin.TabularInline):
    model = ChapterSocialLink
    extra = 1


class PaperTotalInline(admin.TabularInline):
    model = PaperTotal
    extra = 1


@admin.register(Chapter)
class ChapterAdmin(ObjectPermissionsModelAdmin):
    list_display = ('title', 'created')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ['title']}

    inlines = [
        ChapterRoleInline,
        ChapterSocialLinkInline,
        ChapterStateInline,
        ChapterZipInline,
        PaperTotalInline,
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
