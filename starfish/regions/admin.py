from django.contrib import admin

from .models import State, Zip


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Zip)
class ZipAdmin(admin.ModelAdmin):
    search_fields = ['code']
