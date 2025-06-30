import random

import factory
from chapters.models import Chapter, get_chapter_for_zip
from chapters.test_helpers.factories import ChapterFactory
from factory.django import DjangoModelFactory
from faker import Faker
from members.models import ExpungedMember, Member, PendingMember, RemovedMember
from partners.test_helpers.factories import PartnerCampaignFactory
from regions.models import Zip
from users.test_helpers.factories import UserFactory

fake = Faker()


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

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


class PendingMemberFactory(DjangoModelFactory):
    class Meta:
        model = PendingMember

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    zip_code = factory.Iterator(Zip.objects.all())
    chapter = factory.Iterator(Chapter.objects.all())
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    referer_full = factory.Faker('url')


class RemovedMemberFactory(DjangoModelFactory):
    class Meta:
        model = RemovedMember

    status = factory.Iterator(['unsubscribed', 'deleted', 'bounced'])
    removed_by = factory.SubFactory(UserFactory)
    notes = factory.Faker('sentence')


class ExpungedMemberFactory(DjangoModelFactory):
    class Meta:
        model = ExpungedMember

    chapter = factory.SubFactory(ChapterFactory)
    partner_campaign = factory.SubFactory(PartnerCampaignFactory)
    validated = factory.LazyFunction(timezone.now)
