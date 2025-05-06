from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Additional fields and methods can be added here

    def is_chapter_facilitator(self, chapter):
        """
        Returns True if the user is a facilitator of the given chapter.
        """
        if not chapter:
            return False
        return self.chapter_roles.filter(chapter=chapter, role='facilitator').exists()

    def is_chapter_assistant(self, chapter):
        """
        Returns True if the user is an assistant of the given chapter.
        """
        if not chapter:
            return False
        return self.chapter_roles.filter(chapter=chapter, role='assistant').exists()

    def is_chapter_member(self, chapter):
        """
        Returns True if the user is either a facilitator or assistant of the given chapter.
        """
        return self.is_chapter_facilitator(chapter) or self.is_chapter_assistant(chapter)

    def get_user_chapters(self):
        """
        Returns a queryset of chapters where the user has a role.
        """
        from chapters.models import Chapter  # Import here to avoid circular import
        return Chapter.objects.filter(roles__user=self).distinct()
