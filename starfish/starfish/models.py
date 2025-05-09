from django.contrib.auth import get_permission_codename
from django.db import models


class SoftDeletablePermissionManagerMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        request = getattr(self, '_request_user', None)
        if request is None:
            return qs

        opts = self.model._meta
        perm = f"{opts.app_label}.{get_permission_codename('delete', opts)}"
        if request.has_perm(perm):
            return qs
        return qs.filter(is_removed=False)

    def with_user(self, user):
        self._request_user = user
        return self


class SoftDeletablePermissionManager(
    SoftDeletablePermissionManagerMixin, models.Manager
):
    pass
