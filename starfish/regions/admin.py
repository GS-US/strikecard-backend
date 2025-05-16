from django.contrib import admin

from .models import State, Zip


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    list_display_links = list_display
    search_fields = ['code', 'name']


@admin.register(Zip)
class ZipAdmin(admin.ModelAdmin):
    list_display = ['state', 'code']
    list_display_links = list_display
    search_fields = [
        'code',
        'state__code',
        'state__name',
    ]
    list_filter = ['state']
