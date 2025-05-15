import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from chapters.models import Chapter
from chapters.tests.factories import ChapterFactory
from contacts.models import Contact, ExpungedContact, PendingContact, RemovedContact
from partners.tests.factories import PartnerCampaignFactory
from regions.models import Zip
from users.tests.factories import UserFactory


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    zip_code = factory.Iterator(Zip.objects.all())
    chapter = factory.Iterator(Chapter.objects.all())
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    referer_full = factory.Faker('url')
    validated = factory.LazyFunction(timezone.now)


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
