import factory
from starfish.partners.models import PartnerCampaign, Affiliate, Pledge
from starfish.users.models import User

class PartnerCampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartnerCampaign

    name = factory.Faker('company')
    email = factory.Faker('email')
    url = factory.Faker('url')
    key_string = factory.Faker('uuid4')
    legacy_source = factory.Faker('word')
    notes = factory.Faker('sentence')

class AffiliateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Affiliate

    organization_name = factory.Faker('company')
    contact_email = factory.Faker('email')
    notes = factory.Faker('sentence')

class PledgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pledge

    affiliate = factory.SubFactory(AffiliateFactory)
    count = factory.Faker('random_int', min=1, max=100)
    submitted_by_user = factory.SubFactory('starfish.users.tests.factories.UserFactory')
    notes = factory.Faker('sentence')
