from django.core.management.base import BaseCommand
from chapters.models import Chapter
from contacts.models import Contact
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Adds 10 contacts to each chapter'

    def handle(self, *args, **options):
        chapters = Chapter.objects.all()
        for chapter in chapters:
            for i in range(10):
                Contact.objects.create(
                    name=f'Contact {i+1} for {chapter.title}',
                    email=f'{get_random_string(10)}@example.com',
                    zip_code='12345',
                    chapter=chapter,
                )
        self.stdout.write(self.style.SUCCESS('Successfully added 10 contacts to each chapter'))
