import random

import factory
from chapters.models import Chapter, get_chapter_for_zip
from chapters.test_helpers.factories import ChapterFactory
from contacts.models import (Contact, ExpungedContact, PendingContact,
                             RemovedContact)
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker
from partners.test_helpers.factories import PartnerCampaignFactory
from regions.models import Zip
from users.test_helpers.factories import UserFactory

fake = Faker()


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    zip_code = factory.LazyFunction(lambda: Zip.objects.order_by('?').first())
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    referer_full = factory.Faker('url')
    validated = factory.LazyFunction(
        lambda: timezone.make_aware(
            fake.date_time_between(start_date="-3y"), timezone.get_current_timezone()
        )
    )

    @factory.lazy_attribute
    def chapter(self):
        return get_chapter_for_zip(self.zip_code)


class PendingContactFactory(DjangoModelFactory):
    class Meta:
        model = PendingContact

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    zip_code = factory.Iterator(Zip.objects.all())
    chapter = factory.Iterator(Chapter.objects.all())
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    referer_full = factory.Faker('url')


class RemovedContactFactory(DjangoModelFactory):
    class Meta:
        model = RemovedContact

    status = factory.Iterator(['unsubscribed', 'deleted', 'bounced'])
    removed_by = factory.SubFactory(UserFactory)
    notes = factory.Faker('sentence')


class ExpungedContactFactory(DjangoModelFactory):
    class Meta:
        model = ExpungedContact

    chapter = factory.SubFactory(ChapterFactory)
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    validated = factory.LazyFunction(timezone.now)
