from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from chapters.tests.factories import ChapterFactory

class Command(BaseCommand):
    help = "Setup default dev data"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")

        # Create sample chapters using factories
        chapter_titles = [
            "Oregon",
            "New York",
            "No California",
            "So California",
            "Northeastern States",
        ]

        for title in chapter_titles:
            ChapterFactory(title=title)

