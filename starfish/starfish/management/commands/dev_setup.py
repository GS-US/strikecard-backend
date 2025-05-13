from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from chapters.tests.factories import (
    ChapterFactory,
    ChapterRoleFactory,
    ChapterZipFactory,
    ChapterStateFactory,
    ChapterSocialLinkFactory,
    PaperTotalFactory,
)
from contacts.tests.factories import (
    ContactFactory,
    PendingContactFactory,
    RemovedContactFactory,
    ExpungedContactFactory,
)
from partners.tests.factories import (
    PartnerCampaignFactory,
    AffiliateFactory,
    PledgeFactory,
)
from users.tests.factories import UserFactory

class Command(BaseCommand):
    help = 'Setup default dev data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        # Create multiple PendingContact instances
        for _ in range(5):
            PendingContactFactory()

        # Create multiple RemovedContact instances
        for _ in range(5):
            RemovedContactFactory()

        # Create multiple ExpungedContact instances
        for _ in range(5):
            ExpungedContactFactory()

        # Create multiple PartnerCampaign instances
        partner_campaigns = []
        for _ in range(3):
            pc = PartnerCampaignFactory()
            partner_campaigns.append(pc)

        # Create multiple Affiliate instances
        affiliates = []
        for _ in range(3):
            affiliate = AffiliateFactory()
            affiliates.append(affiliate)

        # For each affiliate, create multiple Pledge instances
        for affiliate in affiliates:
            for _ in range(2):
                PledgeFactory(affiliate=affiliate)

        # Assign PartnerCampaigns to some Contacts
        for contact in ContactFactory.create_batch(5):
            contact.partner_campaign = random.choice(partner_campaigns)
            contact.save()

        # Assign PartnerCampaigns to some PendingContacts
        for pending_contact in PendingContactFactory.create_batch(5):
            pending_contact.partner_campaign = random.choice(partner_campaigns)
            pending_contact.save()

        # Create additional users and assign ChapterRoles
        for _ in range(5):
            user = UserFactory()
            ChapterRoleFactory(user=user, chapter=random.choice(chapters), role='assistant')

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
            # Existing code to create users and contacts...

            # Create multiple ChapterZip instances
            for _ in range(3):
                ChapterZipFactory(chapter=chapter)

            # Create multiple ChapterState instances
            for _ in range(2):
                ChapterStateFactory(chapter=chapter)

            # Create multiple ChapterSocialLink instances
            for _ in range(2):
                ChapterSocialLinkFactory(chapter=chapter)

            # Create multiple PaperTotal instances
            for _ in range(5):
                PaperTotalFactory(chapter=chapter)
            for _ in range(2):
                user = UserFactory()
                ChapterRoleFactory(chapter=chapter, user=user)

            # Create 10 contacts for the chapter
            for _ in range(10):
                ContactFactory(chapter=chapter)
