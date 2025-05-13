from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from chapters.models import (
    Chapter,
    ChapterZip,
    ChapterState,
    ChapterRole,
    ChapterSocialLink,
    PaperTotal,
)
from contacts.models import PendingContact, Contact
from partners.models import PartnerCampaign, Affiliate, Pledge


class Command(BaseCommand):
    help = "Setup default dev data"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
