import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from chapters.tests.factories import (
    ChapterFactory,
    ChapterRoleFactory,
    ChapterSocialLinkFactory,
    ChapterStateFactory,
    ChapterZipFactory,
    PaperTotalFactory,
)
from contacts.tests.factories import (
    ContactFactory,
    ExpungedContactFactory,
    PendingContactFactory,
    RemovedContactFactory,
)
from partners.tests.factories import (
    AffiliateFactory,
    PartnerCampaignFactory,
    PledgeFactory,
)
from users.tests.factories import UserFactory


class Command(BaseCommand):
    help = 'Setup default dev data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        admin = User.objects.filter(username='admin')
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        partner_campaigns = []
        for _ in range(3):
            pc = PartnerCampaignFactory()
            partner_campaigns.append(pc)

        for _ in range(3):
            affiliate = AffiliateFactory()
            for _ in range(2):
                PledgeFactory(affiliate=affiliate, submitted_by_user=admin)

        chapter_titles = [
            'Oregon',
            'New York',
            'Northern California',
            'Southern California',
            'Northeastern States',
        ]

        for title in chapter_titles:
            chapter = ChapterFactory(title=title)

            users = []
            for _ in range(2):
                user = UserFactory(is_staff=True)
                users.append(user)
                ChapterRoleFactory(chapter=chapter, user=user, added_by_user=admin)

            if random.random() < 0.8:
                for _ in range(random.randint(1, 3)):
                    ChapterStateFactory(chapter=chapter)
            else:
                for _ in range(random.randint(20, 50)):
                    ChapterZipFactory(chapter=chapter)

            for _ in range(3):
                ChapterSocialLinkFactory(chapter=chapter)

            for _ in range(3):
                PaperTotalFactory(
                    chapter=chapter, submitted_by_user=random.choice(users)
                )

            for _ in range(10):
                partner_campaign = None
                if random.random() < 0.2:
                    partner_campaign = random.choice(partner_campaigns)
                ContactFactory(chapter=chapter, partner_campaign=partner_campaign)

            for _ in range(random.randint(1, 3)):
                PendingContactFactory(chapter=chapter)

            for _ in range(random.randint(1, 3)):
                RemovedContactFactory(removed_by=random.choice(users))

            for _ in range(random.randint(1, 3)):
                ExpungedContactFactory(chapter=chapter)
