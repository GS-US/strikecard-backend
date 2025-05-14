import hashlib
from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from model_utils import FieldTracker
from model_utils.fields import UrlsafeTokenField
from model_utils.managers import SoftDeletableManager
from model_utils.models import SoftDeletableModel, TimeStampedModel
from simple_history.models import HistoricalRecords


class HashedContactRecord(TimeStampedModel):
    email_hash = models.CharField(max_length=128, db_index=True, editable=False)
    phone_hash = models.CharField(
        max_length=128, blank=True, null=True, db_index=True, editable=False
    )


class BaseContact(HashedContactRecord):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.ForeignKey(
        'regions.Zip', on_delete=models.PROTECT, related_name='contacts'
    )
    chapter = models.ForeignKey(
        'chapters.Chapter', on_delete=models.PROTECT, related_name='contacts'
    )
    partner_campaign = models.ForeignKey(
        'partners.PartnerCampaign', on_delete=models.SET_NULL, null=True, blank=True
    )
    referer_full = models.TextField(blank=True, null=True)
    referer_host = models.CharField(max_length=255, blank=True, null=True)
    validation_token = UrlsafeTokenField(null=True, blank=True)
    validation_expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract: True

    def update_hashes(self):

        def _hash(s):
            return hashlib.sha256((s + settings.CONTACT_HASH_SALT).encode()).hexdigest()

        if self.email and (not self.pk or self.tracker.has_changed('email')):
            self.email_hash = _hash(self.email)

        if self.phone and (not self.pk or self.tracker.has_changed('phone')):
            self.phone_hash = _hash(self.phone)

    def update_referer_host(self):
        if self.referer_full and not self.referer_host:
            try:
                self.referer_host = urlparse(self.referer_full).netloc.lower()
            except Exception:
                self.referer_host = None


class PendingContact(BaseContact):
    tracker = FieldTracker(fields=['email', 'phone'])

    def validate_token(self, token):
        if self.validation_token != token:
            return False

        if self.token_is_expired():
            return False

        self.is_validated = True
        self.validated = now()
        self.save()
        return True

    def token_is_expired(self):
        return now() > self.validation_expires

    def save(self, *args, **kwargs):
        if not self.pk:
            self.validation_expires = now() + timedelta(days=7)
            self.update_referer_host()
        self.update_hashes()
        super().save(*args, **kwargs)

    def send_validation_email(self):
        validation_link = reverse('validate_contact', args=[self.validation_token])
        send_mail(
            'Please validate your email',
            f'Click the link to validate your email: {validation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )


class Contact(BaseContact):
    validated = models.DateTimeField(null=True, blank=True)

    tracker = FieldTracker(fields=['email', 'phone'])
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.update_hashes()
        super().save(*args, **kwargs)

    def remove(self, status, removed_by=None, notes=''):
        RemovedContact.objects.create(
            id=self.id,
            email_hash=self.email_hash,
            phone_hash=self.phone_hash,
            status=status,
            removed_by=removed_by,
            notes=notes,
        )
        self.delete()

    def expunge(self):
        ExpungedContact.objects.create(
            id=self.id,
            email_hash=self.email_hash,
            phone_hash=self.phone_hash,
            chapter=self.chapter,
            partner_campaign=self.partner_campaign,
            validated=self.validated,
        )
        self.delete()


class RemovedContact(HashedContactRecord):
    STATUS_CHOICES = [
        ('unsubscribed', 'Unsubscribed'),
        ('deleted', 'Deleted'),
        ('bounced', 'Bounced'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    removed = models.DateTimeField(auto_now_add=True)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.status}: {self.email_hash}'


class ExpungedContact(HashedContactRecord):
    chapter = models.ForeignKey(
        'chapters.Chapter', on_delete=models.PROTECT, related_name='expunged_contacts'
    )
    partner_campaign = models.ForeignKey(
        'partners.PartnerCampaign', on_delete=models.SET_NULL, null=True, blank=True
    )
    validated = models.DateTimeField()
    expunged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'expunged: {self.email_hash}'
