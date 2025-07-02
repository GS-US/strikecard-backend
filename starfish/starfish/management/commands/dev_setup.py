import random

from chapters.models import Chapter
from chapters.test_helpers.factories import (
    ChapterLinkFactory,
    ChapterRoleFactory,
    OfflineTotalFactory,
)
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models.signals import post_save
from members.models import Member, RemovedMember
from members.signals import update_chapter_total_on_member_change
from members.test_helpers.factories import (
    MemberFactory,
    PendingMemberFactory,
)
from partners.test_helpers.factories import (
    AffiliateFactory,
    PartnerCampaignFactory,
    PledgeFactory,
)
from users.test_helpers.factories import UserFactory


class Command(BaseCommand):
    help = 'Setup default dev data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--members',
            type=int,
            default=1000,
            help='Number of members to add (default: 1000)',
        )

    def get_partner_campaign(self, threshold=0.2):
        if random.random() < threshold:
            return random.choice(self.partner_campaigns)
        return None

    def handle(self, *args, **options):
        User = get_user_model()
        post_save.disconnect(update_chapter_total_on_member_change, sender=Member)

        admin = User.objects.filter(username='admin').first()
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'a')

        self.partner_campaigns = []
        for _ in range(5):
            try:
                self.partner_campaigns.append(PartnerCampaignFactory())
            except IntegrityError:
                pass

        for _ in range(3):
            affiliate = AffiliateFactory()
            for _ in range(random.randint(0, 3)):
                PledgeFactory(affiliate=affiliate, submitted_by_user=admin)

        for chapter in Chapter.objects.all():
            users = []
            for _ in range(2):
                try:
                    user = UserFactory()
                    users.append(user)
                    ChapterRoleFactory(chapter=chapter, user=user, added_by_user=admin)
                except IntegrityError:
                    pass

            for _ in range(4):
                ChapterLinkFactory(chapter=chapter)

            for _ in range(random.randint(0, 2)):
                OfflineTotalFactory(
                    chapter=chapter, submitted_by_user=random.choice(users)
                )

            for _ in range(random.randint(0, 3)):
                try:
                    PendingMemberFactory(
                        chapter=chapter, partner_campaign=self.get_partner_campaign()
                    )
                except IntegrityError:
                    pass

        for _ in range(options['members']):
            try:
                MemberFactory(partner_campaign=self.get_partner_campaign())
            except IntegrityError:
                pass

        for c in Member.objects.order_by('?')[:10]:
            c.remove(random.choice(RemovedMember.STATUS_CHOICES)[0])

        for c in Member.objects.order_by('?')[:10]:
            c.expunge()

        for chapter in Chapter.objects.all():
            chapter.update_total_members()
