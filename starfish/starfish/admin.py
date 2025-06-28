from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.utils.html import format_html

admin.site.disable_action('delete_selected')

_original_related_wrapper_init = admin_widgets.RelatedFieldWidgetWrapper.__init__


def patched_related_wrapper_init(
    self,
    widget,
    rel,
    admin_site,
    can_add_related=None,
    can_change_related=None,
    can_delete_related=None,
    can_view_related=None,
):
    _original_related_wrapper_init(
        self,
        widget,
        rel,
        admin_site,
        can_add_related=False,
        can_change_related=False,
        can_delete_related=False,
        can_view_related=False,
    )


admin_widgets.RelatedFieldWidgetWrapper.__init__ = patched_related_wrapper_init


class SoftDeletableAdminMixin:

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return self.model.objects.with_user(request.user).get_queryset()

    def has_soft_delete_permission(self, request):
        opts = self.model._meta
        return request.user.has_perm(f"{opts.app_label}.delete_{opts.model_name}")

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if 'is_removed' in fields:
            fields.remove('is_removed')
            fields.append('is_removed')
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if 'is_removed' in readonly:
            readonly.remove('is_removed')

        if not self.has_soft_delete_permission(request):
            readonly.append('is_removed')

        return readonly

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        if 'is_removed' in list_filter:
            list_filter.remove('is_removed')

        if self.has_soft_delete_permission(request):
            list_filter.append('is_removed')

        return list_filter


class ReadOnlyAdminMixin:

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def pretty_button(url, title):
    return format_html(
        '<a class="inline-block bg-primary-600 text-white font-semibold py-1 px-3 rounded text-sm no-underline" href="{}">{}</a>',
        url,
        title,
    )


def pretty_link(url, title):
    return format_html(
        '<a class="text-primary-600 dark:text-primary-500" href="{}">{}</a>', url, title
    )
