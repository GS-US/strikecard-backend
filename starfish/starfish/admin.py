class SoftDeletableAdminMixin:

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
