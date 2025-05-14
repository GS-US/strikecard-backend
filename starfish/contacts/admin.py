import rules
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from chapters.models import ChapterRole
from contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(ObjectPermissionsModelAdmin):
    list_display = (
        'name',
        'email',
        'chapter',
        'partner_campaign',
    )
    search_fields = ('name', 'email')
    list_filter = ('created',)
    autocomplete_fields = ['zip_code']

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('contacts.view_contact', request.user, obj)
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('contacts.change_contact', request.user, obj)
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return rules.test_perm('contacts.add_contact', request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return rules.test_perm('contacts.delete_contact', request.user, obj)
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        user_chapters = ChapterRole.objects.filter(user=request.user).values_list(
            'chapter', flat=True
        )
        return qs.filter(chapter__in=user_chapters)
