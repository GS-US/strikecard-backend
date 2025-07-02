from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    # Username is required for authentication
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )

    # Email is optional since we're not doing email verification
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='email address',
    )

    history = HistoricalRecords()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # email is required for createsuperuser

    def __str__(self):
        return self.email

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
