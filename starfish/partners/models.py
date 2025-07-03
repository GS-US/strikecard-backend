from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from model_utils.models import SoftDeletableModel, TimeStampedModel
from simple_history.models import HistoricalRecords

from starfish.models import SoftDeletablePermissionManager


class PartnerCampaign(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    url = models.URLField('URL', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)
    legacy_source = models.CharField(max_length=255, blank=True, null=True, unique=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    last_used = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletablePermissionManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(PartnerCampaign, self).save(*args, **kwargs)

    def use(self):
        self.last_used = now()
        self.save()

    @classmethod
    def get_or_create_from_source(cls, source):
        if not source:
            return None

        clean_source = source.strip()
        partner, created = cls.objects.get_or_create(
            legacy_source=clean_source,
            defaults={
                'name': clean_source,
                'email': settings.DEFAULT_PARTNER_EMAIL,
            },
        )
        return partner


class Affiliate(TimeStampedModel, SoftDeletableModel):
    organization_name = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    objects = SoftDeletablePermissionManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.organization_name


class Pledge(models.Model):
    affiliate = models.ForeignKey(
        Affiliate, on_delete=models.PROTECT, related_name='pledges'
    )
    count = models.PositiveIntegerField()
    submitted_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Submitted by', on_delete=models.PROTECT
    )
    notes = models.CharField(blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.count)
