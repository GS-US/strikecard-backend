from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from chapters.tests.factories import ChapterFactory, ChapterRoleFactory
from contacts.tests.factories import ContactFactory
from users.tests.factories import UserFactory

class Command(BaseCommand):
    help = 'Setup default dev data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        chapter_titles = [
            'Oregon',
            'New York',
            'Northern California',
            'Southern California',
            'Northeastern States',
        ]

        chapters = []
        for title in chapter_titles:
            chapter = ChapterFactory(title=title)
            chapters.append(chapter)

        for chapter in chapters:
            # Create 3 users and assign them roles in the chapter
            for _ in range(3):
                user = UserFactory()
                ChapterRoleFactory(chapter=chapter, user=user, role='assistant')

            # Create 10 contacts for the chapter
            for _ in range(10):
                ContactFactory(chapter=chapter)
