import uuid

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

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
