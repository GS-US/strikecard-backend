from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    history = HistoricalRecords()

    def is_chapter_facilitator(self, chapter):
        return self.chapter_roles.filter(chapter=chapter, role='facilitator').exists()

    def is_chapter_assistant(self, chapter):
        return self.chapter_roles.filter(chapter=chapter, role='assistant').exists()

    def is_chapter_member(self, chapter):
        return self.is_chapter_facilitator(chapter) or self.is_chapter_assistant(
            chapter
        )

    def get_chapters(self):
        from chapters.models import Chapter

        return Chapter.objects.filter(roles__user=self).distinct()
