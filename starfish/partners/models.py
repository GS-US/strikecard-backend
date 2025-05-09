import datetime

from django.conf import settings
from django.db import models
from model_utils.fields import UrlsafeTokenField
from model_utils.models import SoftDeletableModel, TimeStampedModel
from simple_history.models import HistoricalRecords

from starfish.models import SoftDeletablePermissionManager


class PartnerCampaign(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    url = models.URLField('URL', blank=True, null=True)
    key_string = UrlsafeTokenField(unique=True, max_length=16)
    legacy_source = models.CharField(max_length=255, blank=True, null=True, unique=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletablePermissionManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def use(self):
        self.last_used_at = datetime.now()
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


class Affiliate(models.Model):
    organization_name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, blank=True)  # New notes field

    def __str__(self):
        return self.organization_name


class Pledge(models.Model):
    affiliate = models.ForeignKey(
        Affiliate, on_delete=models.PROTECT, related_name='pledges'
    )
    count = models.PositiveIntegerField()
    submitted_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    notes = models.CharField(blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.affiliate.organization_name} ({self.count})"
