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

        # Create example chapters representing U.S. states
        chapter_ca = Chapter.objects.create(
            title="California",
            slug="california",
            description="Chapter for California.",
            contact_email="contact@california.com",
            website_url="https://california.com",
        )
        chapter_ny = Chapter.objects.create(
            title="New York",
            slug="new-york",
            description="Chapter for New York.",
            contact_email="contact@newyork.com",
            website_url="https://newyork.com",
        )
        chapter_tx = Chapter.objects.create(
            title="Texas",
            slug="texas",
            description="Chapter for Texas.",
            contact_email="contact@texas.com",
            website_url="https://texas.com",
        )
        chapter_fl = Chapter.objects.create(
            title="Florida",
            slug="florida",
            description="Chapter for Florida.",
            contact_email="contact@florida.com",
            website_url="https://florida.com",
        )
        chapter_il = Chapter.objects.create(
            title="Illinois",
            slug="illinois",
            description="Chapter for Illinois.",
            contact_email="contact@illinois.com",
            website_url="https://illinois.com",
        )

        # Create example chapter zips
        ChapterZip.objects.create(chapter=chapter_ca, zip_code="90001", state_code="CA")
        ChapterZip.objects.create(chapter=chapter_ny, zip_code="10001", state_code="NY")
        ChapterZip.objects.create(chapter=chapter_tx, zip_code="73301", state_code="TX")
        ChapterZip.objects.create(chapter=chapter_fl, zip_code="32004", state_code="FL")
        ChapterZip.objects.create(chapter=chapter_il, zip_code="60007", state_code="IL")

        # Create example chapter states
        ChapterState.objects.create(chapter=chapter_ca, state_code="CA")
        ChapterState.objects.create(chapter=chapter_ny, state_code="NY")
        ChapterState.objects.create(chapter=chapter_tx, state_code="TX")
        ChapterState.objects.create(chapter=chapter_fl, state_code="FL")
        ChapterState.objects.create(chapter=chapter_il, state_code="IL")

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
            chapter=chapter_ca,
            role='facilitator',
            title='Lead Facilitator'
        )
        ChapterRole.objects.create(
            user=user2,
            added_by_user=user1,
            chapter=chapter_tx,
            role='assistant',
            title='Assistant Facilitator'
        )
        ChapterRole.objects.create(
            user=user2,
            added_by_user=user2,
            chapter=chapter_ny,
            role='facilitator',
            title='Lead Facilitator'
        )
        ChapterRole.objects.create(
            user=user1,
            added_by_user=user2,
            chapter=chapter_fl,
            role='assistant',
            title='Assistant Facilitator'
        )
        ChapterRole.objects.create(
            user=user2,
            added_by_user=user1,
            chapter=chapter_il,
            role='facilitator',
            title='Lead Facilitator'
        )

        # Create example social links for chapters
        ChapterSocialLink.objects.create(
            chapter=chapter_ca,
            platform="Twitter",
            url="https://twitter.com/chapter_california"
        )
        ChapterSocialLink.objects.create(
            chapter=chapter_ny,
            platform="Facebook",
            url="https://facebook.com/chapter_newyork"
        )
        ChapterSocialLink.objects.create(
            chapter=chapter_tx,
            platform="Instagram",
            url="https://instagram.com/chapter_texas"
        )
        ChapterSocialLink.objects.create(
            chapter=chapter_fl,
            platform="LinkedIn",
            url="https://linkedin.com/company/chapter_florida"
        )
        ChapterSocialLink.objects.create(
            chapter=chapter_il,
            platform="YouTube",
            url="https://youtube.com/chapter_illinois"
        )

        # Create example paper totals
        PaperTotal.objects.create(
            chapter=chapter_ca,
            count=150,
            submitted_by_user=user1,
            notes="Paper total for California."
        )
        PaperTotal.objects.create(
            chapter=chapter_ny,
            count=250,
            submitted_by_user=user2,
            notes="Paper total for New York."
        )
        PaperTotal.objects.create(
            chapter=chapter_tx,
            count=300,
            submitted_by_user=user1,
            notes="Paper total for Texas."
        )
        PaperTotal.objects.create(
            chapter=chapter_fl,
            count=120,
            submitted_by_user=user2,
            notes="Paper total for Florida."
        )
        PaperTotal.objects.create(
            chapter=chapter_il,
            count=180,
            submitted_by_user=user1,
            notes="Paper total for Illinois."
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
            name="Michael Johnson",
            email="michael.johnson@example.com",
            phone="555-123-4567",
            zip_code="94105",
            chapter=chapter_ca,
            referer_full="https://referrer_california.com",
        )
        pending_contact2 = PendingContact.objects.create(
            name="Laura Williams",
            email="laura.williams@example.com",
            phone="555-987-6543",
            zip_code="10001",
            chapter=chapter_ny,
            referer_full="https://referrer_newyork.com",
        )
        # Add more pending contacts for other chapters as needed
        pending_contact3 = PendingContact.objects.create(
            name="David Brown",
            email="david.brown@example.com",
            phone="555-555-5555",
            zip_code="73301",
            chapter=chapter_tx,
            referer_full="https://referrer_texas.com",
        )

        # Create example validated contacts
        contact1 = Contact.objects.create(
            name="Emma Davis",
            email="emma.davis@example.com",
            phone="555-222-3333",
            zip_code="90001",
            chapter=chapter_ca,
            validated=timezone.now(),
        )
        contact2 = Contact.objects.create(
            name="Liam Wilson",
            email="liam.wilson@example.com",
            phone="555-444-5555",
            zip_code="10001",
            chapter=chapter_ny,
            validated=timezone.now(),
        )
        contact3 = Contact.objects.create(
            name="Olivia Martinez",
            email="olivia.martinez@example.com",
            phone="555-666-7777",
            zip_code="73301",
            chapter=chapter_tx,
            validated=timezone.now(),
        )
