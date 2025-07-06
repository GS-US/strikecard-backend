from django.contrib.auth.backends import BaseBackend

from .models import Chapter, ChapterRole


class ChapterRolePermissionBackend(BaseBackend):

    def has_perm(self, user, perm, obj=None):
        if user.is_superuser:
            return True

        if not obj:
            return super().has_perm(user, perm)

        chapter = isinstance(obj, Chapter) and obj or getattr(obj, 'chapter')

        try:
            role = ChapterRole.objects.get(user=user, chapter=chapter)
        except ChapterRole.DoesNotExist:
            return False

        return role.has_perm(perm, obj=obj)
