from django.contrib.auth.backends import BaseBackend

from .models import ChapterRole


class ChapterRolePermissionBackend(BaseBackend):

    def has_perm(self, user, perm, obj=None):
        if user.is_superuser:
            return True

        if obj and hasattr(obj, 'chapter'):
            try:
                role = ChapterRole.objects.get(user=user, chapter=obj.chapter)
            except ChapterRole.DoesNotExist:
                return False

            try:
                app_name, perm_name = perm.split('.')
            except ValueError:
                return False
            method_name = f'{app_name}_can_{perm_name}'

            print(obj)
            print(method_name)
            return getattr(
                role, method_name, lambda: super().has_perm(user, perm, obj=obj)
            )()
        else:
            print('base perm')
            return super().has_perm(user, perm)
