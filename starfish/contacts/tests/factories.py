import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from contacts.models import PendingContact, Contact, RemovedContact, ExpungedContact
from chapters.tests.factories import ChapterFactory
from partners.tests.factories import PartnerCampaignFactory
from users.tests.factories import UserFactory


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    zip_code = factory.Faker('postcode')
    chapter = factory.SubFactory(ChapterFactory)
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    referer_full = factory.Faker('url')
    validated = factory.LazyFunction(timezone.now)


class PendingContactFactory(DjangoModelFactory):
    class Meta:
        model = PendingContact

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    zip_code = factory.Faker('postcode')
    chapter = factory.SubFactory(ChapterFactory)
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    referer_full = factory.Faker('url')
    validation_token = factory.PostGenerationMethodCall('generate_token')
    validation_expires = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(days=7)
    )


class RemovedContactFactory(DjangoModelFactory):
    class Meta:
        model = RemovedContact

    email_hash = factory.Faker('sha256')
    phone_hash = factory.Faker('sha256')
    status = factory.Iterator(['unsubscribed', 'deleted', 'bounced'])
    removed_by = factory.SubFactory(UserFactory)
    notes = factory.Faker('sentence')


class ExpungedContactFactory(DjangoModelFactory):
    class Meta:
        model = ExpungedContact

    email_hash = factory.Faker('sha256')
    phone_hash = factory.Faker('sha256')
    chapter = factory.SubFactory(ChapterFactory)
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    validated = factory.LazyFunction(timezone.now)
