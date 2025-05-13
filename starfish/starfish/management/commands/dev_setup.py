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

        # Create example chapters
        chapter1 = Chapter.objects.create(
            title="Chapter One",
            slug="chapter-one",
            description="The first chapter.",
            contact_email="contact@chapterone.com",
            website_url="https://chapterone.com",
        )
        chapter2 = Chapter.objects.create(
            title="Chapter Two",
            slug="chapter-two",
            description="The second chapter.",
            contact_email="contact@chaptertwo.com",
            website_url="https://chaptertwo.com",
        )

        # Create example chapter zips
        ChapterZip.objects.create(chapter=chapter1, zip_code="12345", state_code="CA")
        ChapterZip.objects.create(chapter=chapter2, zip_code="67890", state_code="NY")

        # Create example chapter states
        ChapterState.objects.create(chapter=chapter1, state_code="CA")
        ChapterState.objects.create(chapter=chapter2, state_code="NY")

        # Ensure additional users exist
        if not User.objects.filter(username="user1").exists():
            user1 = User.objects.create_user("user1", "user1@example.com", "password1")
        else:
            user1 = User.objects.get(username="user1")

        if not User.objects.filter(username="user2").exists():
            user2 = User.objects.create_user("user2", "user2@example.com", "password2")
        else:
            user2 = User.objects.get(username="user2")

        # Create example chapter roles
        ChapterRole.objects.create(
            user=user1,
            added_by_user=user1,
            chapter=chapter1,
            role='facilitator',
            title='Lead Facilitator'
        )
        ChapterRole.objects.create(
            user=user2,
            added_by_user=user1,
            chapter=chapter1,
            role='assistant',
            title='Assistant Facilitator'
        )
        ChapterRole.objects.create(
            user=user2,
            added_by_user=user2,
            chapter=chapter2,
            role='facilitator',
            title='Lead Facilitator'
        )

        # Create example social links for chapters
        ChapterSocialLink.objects.create(
            chapter=chapter1,
            platform="Twitter",
            url="https://twitter.com/chapter_one"
        )
        ChapterSocialLink.objects.create(
            chapter=chapter2,
            platform="Facebook",
            url="https://facebook.com/chapter_two"
        )

        # Create example paper totals
        PaperTotal.objects.create(
            chapter=chapter1,
            count=100,
            submitted_by_user=user1,
            notes="Initial paper total."
        )
        PaperTotal.objects.create(
            chapter=chapter2,
            count=200,
            submitted_by_user=user2,
            notes="Second paper total."
        )

        # Create example partner campaigns
        campaign1 = PartnerCampaign.objects.create(
            name="Campaign One",
            email="campaign1@example.com",
            url="https://campaignone.com",
            notes="First partner campaign."
        )
        campaign2 = PartnerCampaign.objects.create(
            name="Campaign Two",
            email="campaign2@example.com",
            url="https://campaigntwo.com",
            notes="Second partner campaign."
        )

        # Create example affiliates
        affiliate1 = Affiliate.objects.create(
            organization_name="Affiliate One",
            contact_email="affiliate1@example.com",
            notes="Notes about Affiliate One."
        )
        affiliate2 = Affiliate.objects.create(
            organization_name="Affiliate Two",
            contact_email="affiliate2@example.com",
            notes="Notes about Affiliate Two."
        )

        # Create example pledges
        Pledge.objects.create(
            affiliate=affiliate1,
            count=50,
            submitted_by_user=user1,
            notes="First pledge."
        )
        Pledge.objects.create(
            affiliate=affiliate2,
            count=75,
            submitted_by_user=user2,
            notes="Second pledge."
        )

        # Create example pending contacts
        pending_contact1 = PendingContact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            zip_code="12345",
            chapter=chapter1,
            referer_full="https://referrerone.com",
        )
        pending_contact2 = PendingContact.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="987-654-3210",
            zip_code="67890",
            chapter=chapter2,
            referer_full="https://referrertwo.com",
        )

        # Create example validated contacts
        contact1 = Contact.objects.create(
            name="Alice Brown",
            email="alice.brown@example.com",
            phone="555-555-5555",
            zip_code="54321",
            chapter=chapter1,
            validated=timezone.now(),
        )
        contact2 = Contact.objects.create(
            name="Bob Johnson",
            email="bob.johnson@example.com",
            phone="444-444-4444",
            zip_code="98765",
            chapter=chapter2,
            validated=timezone.now(),
        )
