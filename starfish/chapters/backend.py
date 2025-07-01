from django.contrib.auth.backends import BaseBackend

from .roles import get_user_chapter_role


class ChapterRolePermissionBackend(BaseBackend):
    def has_perm(self, user, perm, obj=None):
        if user.is_superuser:
            return True

        try:
            _, perm_name = perm.split('.')
        except ValueError:
            return False

        if not obj or not hasattr(obj, 'chapter'):
            return False

        method_name = f'can_{perm_name}'
        role = get_user_chapter_role(user, obj.chapter)
        return getattr(role, method_name, lambda: False)()
