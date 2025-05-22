from django.core.management.base import BaseCommand
from django.utils.text import slugify
from regions.models import State
from chapters.models import Chapter

class Command(BaseCommand):
    help = 'Creates chapters for every state'

    def handle(self, *args, **kwargs):
        for state in State.objects.all():
            chapter_title = f'{state.name} Chapter'
            chapter_slug = slugify(state.name)
            chapter, created = Chapter.objects.get_or_create(
                slug=chapter_slug,
                defaults={'title': chapter_title}
            )
            if created:
                chapter.states.add(state)
                self.stdout.write(self.style.SUCCESS(f'Created chapter: {chapter_title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Chapter for {state.name} already exists'))
