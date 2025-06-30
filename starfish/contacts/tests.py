import os
from pathlib import PurePath

from contacts.forms import PendingContactForm
from django.core.management import call_command
from django.test import TestCase
from regions.models import Zip

start_dir = PurePath(os.getcwd())
if start_dir.name != "starfish":
    start_dir /= "starfish"


# Create your tests here.
class TestPendingContactForm(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        call_command("loaddata", start_dir / "regions/fixtures/regions.json")

    def test_phone(self):
        success_phones = ("202 202 2020",)
        failure_phones = ()

        for phone in success_phones:
            pcf = PendingContactForm(
                data={
                    "name": "name",
                    "email": "email@domain.com",
                    "zip_code": "20746",
                    "phone": phone,
                }
            )
            is_valid = pcf.is_valid()
            if not is_valid:
                a = Zip.objects.all()
                raise RuntimeError(pcf.errors)
            self.assertEqual(pcf.cleaned_data["phone"], "2022022020")

        for phone in failure_phones:
            pass
