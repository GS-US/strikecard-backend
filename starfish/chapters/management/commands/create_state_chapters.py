import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from chapters.models import Chapter
from regions.models import State, Zip

chapter_exceptions = {
    'NY': ['Greater NY', 'New York City'],
    'CA': ['Northern California', 'Southern California'],
}


class Command(BaseCommand):
    help = 'Creates chapters for every state'

    def _new_chapter(self, state=None, name=None):
        if not name:
            name = state.name

        chapter_slug = slugify(name)
        chapter, created = Chapter.objects.get_or_create(
            slug=chapter_slug,
            defaults={
                'title': name,
                'description': f'{name} Chapter of the General Strike',
            },
        )
        if created and state:
            chapter.states.add(state)
        return chapter

    def handle(self, *args, **kwargs):
        for state in State.objects.exclude(code__in=chapter_exceptions.keys()):
            self._new_chapter(state)

        for state_code, titles in chapter_exceptions.items():
            state = State.objects.get(code=state_code)
            for title in titles:
                chapter = self._new_chapter(state=state, name=title)
                zips = Zip.objects.filter(state__code=state_code).order_by('?')[
                    : random.randint(5, 50)
                ]
                for z in zips:
                    try:
                        chapter.zips.create(zip_code=z)
                    except:
                        pass
