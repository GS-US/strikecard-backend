import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterState,
    ChapterZip,
    PaperTotal,
)
from users.tests.factories import UserFactory


class ChapterFactory(DjangoModelFactory):
    class Meta:
        model = Chapter

    title = factory.Faker('state', nb_words=4)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker('catch_phrase')
    contact_email = factory.Faker('email')
    website_url = factory.Faker('url')


class ChapterZipFactory(DjangoModelFactory):
    class Meta:
        model = ChapterZip

    chapter = factory.SubFactory(ChapterFactory)
    zip_code = factory.Faker('postcode')
    state_code = factory.Faker('state_abbr')


class ChapterStateFactory(DjangoModelFactory):
    class Meta:
        model = ChapterState

    chapter = factory.SubFactory(ChapterFactory)
    state_code = factory.Faker('state_abbr')


class ChapterRoleFactory(DjangoModelFactory):
    class Meta:
        model = ChapterRole

    user = factory.SubFactory(UserFactory)
    added_by_user = factory.SubFactory(UserFactory)
    chapter = factory.SubFactory(ChapterFactory)
    role = factory.Iterator(['facilitator', 'assistant'])
    title = factory.Iterator(['facilitator', 'assistant'])


class ChapterSocialLinkFactory(DjangoModelFactory):
    class Meta:
        model = ChapterSocialLink

    chapter = factory.SubFactory(ChapterFactory)
    platform = factory.Iterator(['Discord', 'Bluesky', 'Substack'])
    url = factory.Faker('url')


class PaperTotalFactory(DjangoModelFactory):
    class Meta:
        model = PaperTotal

    chapter = factory.SubFactory(ChapterFactory)
    count = factory.Faker('random_int', min=1, max=1000)
    submitted_by_user = factory.SubFactory(UserFactory)
    notes = factory.Faker('catch_phrase')
