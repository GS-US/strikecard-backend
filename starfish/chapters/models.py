from django.conf import settings
from django.db import models
from model_utils.managers import SoftDeletableManager
from model_utils.models import SoftDeletableModel, TimeStampedModel
from simple_history.models import HistoricalRecords

from regions.models import State, Zip

class Chapter(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    zips = models.ManyToManyField('regions.Zip', related_name='chapters')
    states = models.ManyToManyField('regions.State', related_name='chapters')

    objects = SoftDeletableManager()
    history = HistoricalRecords()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title




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
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
