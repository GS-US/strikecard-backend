from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from chapters.models import get_chapter_for_zip
from starfish.admin import ReadOnlyAdminMixin

from .models import State, Zip


@admin.register(State)
class StateAdmin(ReadOnlyAdminMixin, ModelAdmin):
    list_display = ['code', 'name']
    list_display_links = list_display
    search_fields = list_display
    fields = list_display + ['zip_codes']
    readonly_fields = fields
    compressed_fields = True

    def zip_codes(self, obj):
        url = (
            reverse('admin:regions_zip_changelist') + f'?state__code__exact={obj.code}'
        )
        return format_html('<a href="{}">View ZIP Codes</a>', url)

    zip_codes.short_description = 'ZIP Codes'


@admin.register(Zip)
class ZipAdmin(ReadOnlyAdminMixin, ModelAdmin):
    list_display = ['state', 'code']
    list_display_links = ['code']
    search_fields = [
        'code',
        'state__code',
        'state__name',
    ]
    list_filter = ['state']
    fields = ['state', 'code', 'associated_chapter']
    readonly_fields = fields
    compressed_fields = True

    def associated_chapter(self, obj):
        chapter = get_chapter_for_zip(obj)
        if chapter:
            url = reverse('admin:chapters_chapter_change', args=[chapter.id])
            return format_html('<a href="{}">{}</a>', url, chapter.title)
        else:
            return 'No Chapter'

    associated_chapter.short_description = 'Chapter'
