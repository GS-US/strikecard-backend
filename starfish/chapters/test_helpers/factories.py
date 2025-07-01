import factory
from chapters.models import Chapter, ChapterRole, ChapterSocialLink, OfflineTotal
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from regions.models import State, Zip
from users.test_helpers.factories import UserFactory


class ChapterFactory(DjangoModelFactory):
    class Meta:
        model = Chapter

    title = factory.Faker('state', nb_words=4)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker('catch_phrase')
    contact_email = factory.Faker('email')
    website_url = factory.Faker('url')


class ChapterRoleFactory(DjangoModelFactory):
    class Meta:
        model = ChapterRole

    user = factory.SubFactory(UserFactory)
    added_by_user = factory.SubFactory(UserFactory)
    chapter = factory.SubFactory(ChapterFactory)


class ChapterSocialLinkFactory(DjangoModelFactory):
    class Meta:
        model = ChapterSocialLink

    chapter = factory.SubFactory(ChapterFactory)
    platform = factory.Iterator(['Discord', 'Bluesky', 'Substack'])
    url = factory.Faker('url')


class OfflineTotalFactory(DjangoModelFactory):
    class Meta:
        model = OfflineTotal

    chapter = factory.SubFactory(ChapterFactory)
    count = factory.Faker('random_int', min=1, max=1000)
    submitted_by_user = factory.SubFactory(UserFactory)
    notes = factory.Faker('catch_phrase')
