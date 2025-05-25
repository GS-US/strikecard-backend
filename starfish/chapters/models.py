from django.conf import settings
from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel
from simple_history.models import HistoricalRecords

from regions.models import State, Zip
from starfish.models import SoftDeletablePermissionManager


def get_chapter_for_zip(zip_code):
    if not zip_code:
        return None

    if type(zip_code) == str:
        zip_code = Zip.objects.get(code=zip_code)

    try:
        return ChapterZip.objects.get(zip_code=zip_code.code).chapter
    except (ChapterZip.DoesNotExist, Chapter.DoesNotExist):
        try:
            return Chapter.objects.filter(states=zip_code.state_id).first()
        except Chapter.DoesNotExist:
            try:
                return Chapter.objects.get(slug='national')
            except Chapter.DoesNotExist:
                return None


class Chapter(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website_url = models.URLField('Website', blank=True, null=True)
    states = models.ManyToManyField(
        'regions.State', related_name='chapters', blank=True
    )

    objects = SoftDeletablePermissionManager()
    history = HistoricalRecords()

    class Meta:
        ordering = (
            'states__name',
            'title',
        )

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
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='added_roles',
        editable=False,
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='assistant')
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.get_role_display()


class ChapterSocialLink(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='social_links'
    )
    platform = models.CharField(max_length=50)
    url = models.URLField('URL')

    history = HistoricalRecords()

    def __str__(self):
        return self.platform


class ChapterZip(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='zips')
    zip_code = models.ForeignKey(Zip, on_delete=models.PROTECT, related_name='chapters')
    state = models.ForeignKey(State, on_delete=models.PROTECT, editable=False)

    class Meta:
        verbose_name = 'Chapter ZIP'
        ordering = ('zip_code',)

    def __str__(self):
        return str(self.zip_code)

    def save(self, *args, **kwargs):
        if not self.state_id:
            self.state = self.zip_code.state
        super().save(*args, **kwargs)


class PaperTotal(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='paper_totals'
    )
    count = models.PositiveIntegerField()
    submitted_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False
    )
    notes = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.created.strftime('%b %d, %Y')
