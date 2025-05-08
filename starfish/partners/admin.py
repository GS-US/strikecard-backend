from django.contrib import admin

from .models import PartnerCampaign


@admin.register(PartnerCampaign)
class PartnerCampaignAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'url',
        'last_used_at',
    )
    search_fields = ('name', 'email', 'url', 'legacy_source')
    list_filter = ('created', 'modified', 'is_removed')
    readonly_fields = ('key_string', 'created', 'modified', 'last_used_at')

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly.append("is_removed")
        return readonly
