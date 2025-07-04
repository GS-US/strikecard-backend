import os
import textwrap
from pathlib import PurePath

from django.core.management import call_command
from django.test import TestCase
from members.forms import PendingMemberForm
from regions.models import Zip

start_dir = PurePath(os.getcwd())
if start_dir.name != "starfish":
    start_dir /= "starfish"


# Create your tests here.
class TestPendingMemberForm(TestCase):
    GENERAL_ERROR = (
        textwrap.dedent(
            r"""
            Please enter a 10-digit North American phone number without the 1.
             Spaces and the following punctuation are allowed: ().-
            """
        )
        .strip()
        .replace("\n", "")
    )
    AREA_CODE_ERROR = (
        textwrap.dedent(
            r"""
            Please ensure your phone number has a valid area code.
             Area codes cannot start with 0 or 1,
             cannot have the second digit be 9,
             and cannot have the second and third digit be the same.
            """
        )
        .strip()
        .replace("\n", "")
    )
    PREFIX_CODE_ERROR = (
        textwrap.dedent(
            r"""
            Please ensure your three-digit prefix (exchange) is valid.
             Prefixes cannot start with 0 or 1, cannot be 555, and cannot
             have the second and third digit both be 1.
            """
        )
        .strip()
        .replace("\n", "")
    )

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("loaddata", start_dir / "regions/fixtures/regions.json")

    def test_phone(self):
        success_phones = {
            "202 212 2220": "2022122220",
            "404 444 4040": "4044444040",
            "4054054050": "4054054050",
            "(405) 405-4050": "4054054050",
            "405-405-4050": "4054054050",
            "405.405.4050": "4054054050",
        }
        failure_phones = {
            # GENERAL ERRORS
            "": self.GENERAL_ERROR,
            "1": self.GENERAL_ERROR,
            "22": self.GENERAL_ERROR,
            "203": self.GENERAL_ERROR,
            "2034": self.GENERAL_ERROR,
            "20345": self.GENERAL_ERROR,
            "203456": self.GENERAL_ERROR,
            "2034567": self.GENERAL_ERROR,
            "20345678": self.GENERAL_ERROR,
            "203456789": self.GENERAL_ERROR,
            "a": self.GENERAL_ERROR,
            # AREA CODE ERRORS
            "012 345 6789": self.AREA_CODE_ERROR,  # leading 0
            "102 345 6789": self.AREA_CODE_ERROR,  # leading 1
            "370 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "371 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "372 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "373 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "374 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "375 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "376 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "377 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "378 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "379 234 5678": self.AREA_CODE_ERROR,  # 370-379
            "960 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "961 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "962 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "963 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "964 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "965 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "966 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "967 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "968 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "969 234 5678": self.AREA_CODE_ERROR,  # 960-969
            "950 234 5678": self.AREA_CODE_ERROR,  # 950
            "958 234 5678": self.AREA_CODE_ERROR,  # 958
            "959 234 5678": self.AREA_CODE_ERROR,  # 959
            "911 345 6789": self.AREA_CODE_ERROR,  # 2nd & 3rd same
            "888 234 5678": self.AREA_CODE_ERROR,  # 2nd & 3rd same
            "290 234 5678": self.AREA_CODE_ERROR,  # middle 9
            # PREFIX ERRORS
            "202 012 5678": self.PREFIX_CODE_ERROR,  # leading 0
            "202 102 5678": self.PREFIX_CODE_ERROR,  # leading 1
            "202 555 5678": self.PREFIX_CODE_ERROR,  # 555
            "202 911 5678": self.PREFIX_CODE_ERROR,  # 2nd & 3rd same
        }

        def create_form(phone: str) -> PendingMemberForm:
            return PendingMemberForm(
                data={
                    "name": "name",
                    "email": "email@domain.com",
                    "zip_code": "20746",
                    "phone": phone,
                }
            )

        for actual, expected in success_phones.items():
            pcf = create_form(actual)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(actual, pcf.errors)
            self.assertEqual(pcf.cleaned_data["phone"], expected)

        for failure_phone, expected_error in failure_phones.items():
            pcf = create_form(failure_phone)
            is_valid = pcf.is_valid()
            if is_valid:
                raise RuntimeError(failure_phone)
            for field, errors in pcf.errors.items():
                if field != "phone" or len(errors) != 1:
                    raise RuntimeError
                actual_error = errors[0]
                self.assertEqual(actual_error, expected_error)
