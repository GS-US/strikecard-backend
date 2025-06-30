from string import digits

from django import forms
from partners.models import PartnerCampaign
from regions.models import Zip

from .models import PendingMember, get_by_email

PHONE_PUNCTUATION = r".()- "
PHONE_TRANSLATION_TABLE = str.maketrans("", "", PHONE_PUNCTUATION)


class PendingMemberForm(forms.ModelForm):
    email = forms.CharField(required=True)
    zip_code = forms.CharField(label='5-digit ZIP Code', min_length=5, max_length=5)
    partner_slug = forms.CharField(
        widget=forms.HiddenInput(), max_length=255, required=False
    )

    class Meta:
        model = PendingMember
        fields = [
            'name',
            'email',
            'phone',
            'zip_code',
            'partner_slug',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name = self.fields['name']
        name.widget = forms.TextInput(attrs={'placeholder': 'e.g., Jordan Doe'})

        email = self.fields['email']
        email.widget = forms.EmailInput(attrs={'placeholder': 'e.g., j.doe@abc.com'})

        phone = self.fields['phone']
        phone.widget = forms.TextInput(attrs={'placeholder': 'e.g., 202-555-1234'})

        zip_code = self.fields['zip_code']
        zip_code.widget = forms.TextInput(attrs={'placeholder': 'e.g., 01234'})

    def clean(self):
        partner_slug = self.cleaned_data.get('partner_slug')
        if partner_slug:
            try:
                self.instance.partner_campaign = PartnerCampaign.objects.get(
                    slug=partner_slug
                )
            except PartnerCampaign.DoesNotExist:
                pass

    def clean_zip_code(self):
        zip_code_input = self.cleaned_data.get('zip_code').strip()
        try:
            return Zip.objects.get(code=zip_code_input)
        except Zip.DoesNotExist:
            raise forms.ValidationError('Please enter a valid 5-digit ZIP Code.')

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        member = get_by_email(email)

        if member:
            if isinstance(member, PendingMember):
                member.delete()
            else:
                raise forms.ValidationError(
                    'The email address entered is already registered.'
                )
        return email

    def clean_phone(self):
        """Validate NANP Telephone Numbers

        https://en.wikipedia.org/wiki/North_American_Numbering_Plan#Modern_plan

        Telephone numbers have the following form: NXX-NXX-XXXX per the "North
        American Numbering Plan"

        - Exactly 10 digits
        - N must be 2-9
        - X may be 0-9 with some exceptions.

        Additional rules:

        - First NXX is the area code.
            - Reserved and non-geographic codes.
                - NXX where the two X are identical, reserved for non-geographic
                  use. 911, 988, 800, etc.
                - N90-N99 are reserved for expansion.
                - 370-379, 960-969 are reserved for expansion.
                - 880-889 are reserved for toll-free use.
                - 950 is reserved for usage of prepaid calling cards.
                - 958, 959 are reserved for system testing.
        - Second NXX is the prefix (or exchange).
            - Prefixes of the form N11 were reserved for "Easily Recognizable
              Codes" during the transition to the modern plan and, while we must
              dial with 10 digits now, this rule has stuck around.
            - Prefix 555 has a block of line numbers reserved for fictional use.
              Only two line numbers (1212, 4334) are currently in use, the
              others are reserved until a need is approved by the Industry
              Numbering Committee:
              https://www.nanpa.com/numbering/555-line-numbers. We can reject
              any of these numbers at this time.
        - XXXX is the line number. There are no restrictions.
        """
        phone_input = self.cleaned_data.get("phone")

        if not phone_input:
            return None

        if not isinstance(phone_input, str):
            msg = "Phone number not a string."
            raise RuntimeError(msg)

        VERIFICATION_MSG = (
            "Please enter a 10-digit North American phone number without the 1."
            "\n Spaces and the following punctuation are allowed: ().-"
        )

        if not _is_phone_input_only_allowed_characters(phone_input):
            raise forms.ValidationError(VERIFICATION_MSG)

        phone_input = _remove_punctuation_and_space(phone_input)

        if not len(phone_input) == 10:
            raise forms.ValidationError(VERIFICATION_MSG)

        area_code = phone_input[:3]
        if not _is_phone_area_code_valid(area_code):
            msg = (
                "Please ensure your phone number has a valid area code."
                "\nArea codes cannot start with 0 or 1."
            )
            raise forms.ValidationError(msg)

        prefix = phone_input[3:6]
        if not _is_phone_prefix_valid(prefix):
            msg = (
                "Please ensure your three-digit prefix (exchange) is valid."
                "\nPrefixes cannot start with 0 or 1, and cannot be 555."
            )
            raise forms.ValidationError(msg)

        return phone_input


def _is_phone_input_only_allowed_characters(v):
    return set(v) <= set(PHONE_PUNCTUATION + digits)


def _remove_punctuation_and_space(v):
    return v.translate(PHONE_TRANSLATION_TABLE)


def _is_phone_area_code_valid(v):
    return _is_phone_nanp_n_digit_valid(v) and _is_phone_area_code_geographic(v)


def _is_phone_area_code_geographic(v):
    return not (
        _is_phone_easily_recognizable_code(v)
        or v[1] == "9"  # Reserved for 12-digit expansion plan
        or v[:2] in ("37", "88", "96")  # Reserved for non-geographic use
        or v in ("950", "958", "959")  # Reserved for non-geographic use
    )


def _is_phone_prefix_valid(v):
    return _is_phone_nanp_n_digit_valid(v) and not _is_phone_prefix_reserved(v)


def _is_phone_prefix_reserved(v):
    return v == "555"  # Reserved for special use


def _is_phone_easily_recognizable_code(v):
    return v[1] == v[2]


def _is_phone_nanp_n_digit_valid(v):
    return v[0] not in ("0", "1")
