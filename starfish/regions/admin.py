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
    compressed_fields = True

    def zip_codes(self, obj):
        url = reverse('admin:regions_zip_changelist')
        url += f'?state__code__exact={obj.code}'
        return format_html(
            '<a class="inline-block bg-primary-600 text-white font-semibold py-1 px-3 rounded text-sm no-underline" href="{}">View ZIP Codes</a>',
            url,
        )

    zip_codes.short_description = 'ZIP Codes'


@admin.register(Zip)
class ZipAdmin(ReadOnlyAdminMixin, ModelAdmin):
    list_display = ['state', 'code', 'type', 'county', 'population']
    list_display_links = list_display
    search_fields = [
        'code',
        'state__code',
        'state__name',
        'primary_city',
        'county',
        'acceptable_cities',
    ]
    list_filter = [
        'type',
        'state',
    ]
    fields = [
        (
            'code',
            'type',
        ),
        'state',
        ('county', 'primary_city'),
        'acceptable_cities',
        (
            'timezone',
            'area_codes',
        ),
        (
            'latitude',
            'longitude',
        ),
        'population',
    ]
    compressed_fields = True

    def associated_chapter(self, obj):
        chapter = get_chapter_for_zip(obj)
        if chapter:
            url = reverse('admin:chapters_chapter_change', args=[chapter.id])
            return format_html('<a href="{}">{}</a>', url, chapter.title)
        else:
            return 'No Chapter'

    associated_chapter.short_description = 'Chapter'
