import hashlib
from datetime import timedelta
from urllib.parse import urlparse

from chapters.models import get_chapter_for_zip
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from model_utils import FieldTracker
from model_utils.fields import UrlsafeTokenField
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

User = get_user_model()


def hash_str(s):
    return hashlib.sha256((s + settings.CONTACT_HASH_SALT).encode()).hexdigest()


def get_by_email(email):
    try:
        hc = HashedContactRecord.objects.get(email_hash=hash_str(email))
        return hc.get_real_instance()
    except HashedContactRecord.DoesNotExist:
        pass


class HashedContactRecord(TimeStampedModel):
    CHILD_ATTRS = ['pendingcontact', 'contact', 'expungedcontact', 'removedcontact']

    email_hash = models.CharField(
        max_length=128, unique=True, db_index=True, editable=False
    )

    def get_real_instance(self):
        for attr in self.CHILD_ATTRS:
            try:
                return getattr(self, attr)
            except ObjectDoesNotExist:
                continue


class BaseContact(HashedContactRecord):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.ForeignKey(
        'regions.Zip', on_delete=models.PROTECT, related_name='%(class)ss'
    )
    chapter = models.ForeignKey(
        'chapters.Chapter',
        on_delete=models.PROTECT,
        related_name='%(class)ss',
        null=True,
        blank=True,
    )
    partner_campaign = models.ForeignKey(
        'partners.PartnerCampaign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)ss',
    )
    referer_full = models.TextField('Referrer', blank=True, null=True)
    referer_host = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.update_referer_host()
        self.assign_chapter()
        self.update_email_hash()

        if self.partner_campaign and (
            not self.pk or self.tracker.has_changed('partner_campaign')
        ):
            self.partner_campaign.use()

        super().save(*args, **kwargs)

    def assign_chapter(self):
        if self.zip_code and not self.chapter:
            self.chapter = get_chapter_for_zip(self.zip_code)

    def update_email_hash(self):
        if self.email and (not self.pk or self.tracker.has_changed('email')):
            self.email_hash = hash_str(self.email)

    def update_referer_host(self):
        if self.referer_full and not self.referer_host:
            try:
                self.referer_host = urlparse(self.referer_full).netloc.lower()
            except Exception:
                self.referer_host = None


def _get_validation_expires():
    return now() + timedelta(days=7)


class PendingContact(BaseContact):
    validation_token = UrlsafeTokenField(max_length=32)
    validation_expires = models.DateTimeField(default=_get_validation_expires)

    tracker = FieldTracker(fields=['email', 'phone', 'partner_campaign'])

    def token_is_expired(self):
        return now() > self.validation_expires

    def validate_contact(self):
        if self.token_is_expired():
            return None

        self.delete()
        contact = Contact.objects.create(
            name=self.name,
            email=self.email,
            phone=self.phone,
            zip_code=self.zip_code,
            chapter=self.chapter,
            partner_campaign=self.partner_campaign,
            referer_full=self.referer_full,
            referer_host=self.referer_host,
            validated=now(),
        )
        return contact

    def get_validation_link(self, request):
        return request.build_absolute_uri(
            reverse('validate_contact', args=[self.validation_token])
        )

    def send_validation_email(self, request):
        validation_link = self.get_validation_link(request)
        print(validation_link)
        return  # don't send until SMTP configured
        send_mail(
            'Please validate your email',
            f'Click the link to validate your email: {validation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )


class Contact(BaseContact):
    LEADERSHIP_CHOICES = ((i, str(i)) for i in range(1, 6))
    validated = models.DateTimeField(null=True, blank=True)
    leadership_score = models.SmallIntegerField(
        'Leadership', choices=LEADERSHIP_CHOICES, null=True, blank=True
    )

    tracker = FieldTracker(fields=['email', 'phone', 'partner_campaign'])
    history = HistoricalRecords()

    class Meta:
        ordering = ('-validated',)

    def remove(self, status, removed_by=None, notes=''):
        self.delete()
        RemovedContact.objects.create(
            id=self.id,
            email_hash=self.email_hash,
            status=status,
            removed_by=removed_by,
            notes=notes,
        )

    def expunge(self):
        self.delete()
        ExpungedContact.objects.create(
            id=self.id,
            email_hash=self.email_hash,
            chapter=self.chapter,
            partner_campaign=self.partner_campaign,
            validated=self.validated,
        )


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


class ContactNote(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='notes')
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='contact_notes'
    )
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Note'

    def __str__(self):
        return f'Note by {self.created_by.username} on {self.created.strftime("%Y-%m-%d ")}'

    def save(self, *args, **kwargs):
        if self.pk:
            # Prevent updates to existing notes
            return
        super().save(*args, **kwargs)
