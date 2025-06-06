from django.contrib import admin
from django.urls import reverse
from unfold.admin import ModelAdmin

from chapters.models import get_chapter_for_zip
from starfish.admin import ReadOnlyAdminMixin, pretty_button, pretty_link

from .models import State, Zip


@admin.register(State)
class StateAdmin(ReadOnlyAdminMixin, ModelAdmin):
    list_display = ['code', 'name']
    list_display_links = list_display
    search_fields = list_display
    fields = list_display + ['zip_codes']
    compressed_fields = True

    def zip_codes(self, obj):
        return pretty_button(
            reverse('admin:regions_zip_changelist') + f'?state__code__exact={obj.code}',
            'View ZIP Codes',
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
        (
            'state',
            'associated_chapter',
        ),
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
            return pretty_link(
                reverse('admin:chapters_chapter_change', args=[chapter.id]),
                chapter.title,
            )
        else:
            return None

    associated_chapter.short_description = 'Chapter'
