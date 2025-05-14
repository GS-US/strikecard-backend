import factory

from partners.models import Affiliate, PartnerCampaign, Pledge
from users.models import User


class PartnerCampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartnerCampaign

    name = factory.Faker('company')
    email = factory.Faker('email')
    url = factory.Faker('url')
    legacy_source = factory.Faker('word')
    notes = factory.Faker('sentence')


class AffiliateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Affiliate

    organization_name = factory.Faker('company')
    contact_email = factory.Faker('email')
    notes = factory.Faker('catch_phrase')


class PledgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pledge

    affiliate = factory.SubFactory(AffiliateFactory)
    count = factory.Faker('random_int', min=100, max=100000)
    submitted_by_user = factory.SubFactory('users.tests.factories.UserFactory')
    notes = factory.Faker('sentence')
