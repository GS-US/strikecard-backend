from django.contrib import admin

from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterState,
    ChapterZip,
    PaperTotal,
)
from rules.contrib.admin import ObjectPermissionsModelAdmin


class ChapterZipInline(admin.TabularInline):
    model = ChapterZip
    extra = 1


class ChapterStateInline(admin.TabularInline):
    model = ChapterState
    extra = 1


import rules


class ChapterSocialLinkInline(admin.TabularInline):
    model = ChapterSocialLink
    extra = 1


class PaperTotalInline(admin.TabularInline):
    model = PaperTotal
    extra = 1


class ChapterAdmin(ObjectPermissionsModelAdmin):
    list_display = ('title', 'slug', 'contact_email')
    search_fields = ('title', 'slug')
    list_filter = ('created', 'modified')

    inlines = [
        ChapterZipInline,
        ChapterStateInline,
        ChapterRoleInline,
        ChapterSocialLinkInline,
        PaperTotalInline,
    ]

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('chapters.view_chapter', request.user, obj)
        return True  # Allow viewing the list

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('chapters.change_chapter', request.user, obj)
        return False
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_chapters = ChapterRole.objects.filter(user=request.user).values_list(
            'chapter', flat=True
        )
        return qs.filter(id__in=user_chapters)


admin.site.register(Chapter, ChapterAdmin)
