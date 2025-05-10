from django.conf import settings
from django.db import models
from model_utils.managers import SoftDeletableManager
from model_utils.models import SoftDeletableModel, TimeStampedModel
from simple_history.models import HistoricalRecords


class Chapter(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    objects = SoftDeletableManager()
    history = HistoricalRecords()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class ChapterZip(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='zips')
    zip_code = models.CharField(max_length=10, unique=True)
    state_code = models.CharField(max_length=2)


class ChapterState(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='states'
    )
    state_code = models.CharField(max_length=2)


class ChapterRole(models.Model):
    ROLE_CHOICES = [
        ('facilitator', 'Facilitator'),
        ('assistant', 'Assistant'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='chapter_roles'
    )
    added_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='added_roles'
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='assistant')
    title = models.CharField(
        max_length=255, blank=True, null=True, default='Facilitator'
    )


class ChapterSocialLink(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='social_links'
    )
    platform = models.CharField(max_length=50)
    url = models.URLField()

    history = HistoricalRecords()


class PaperTotal(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='paper_totals'
    )
    count = models.PositiveIntegerField()
    submitted_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
