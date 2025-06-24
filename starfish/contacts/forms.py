from django import forms
from partners.models import PartnerCampaign
from regions.models import Zip

from .models import PendingContact, get_by_email


class PendingContactForm(forms.ModelForm):
    email = forms.CharField(required=True)
    zip_code = forms.CharField(label='5-digit ZIP Code', min_length=5, max_length=5)
    partner_slug = forms.CharField(
        widget=forms.HiddenInput(), max_length=255, required=False
    )

    class Meta:
        model = PendingContact
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
        contact = get_by_email(email)

        if contact:
            if isinstance(contact, PendingContact):
                contact.delete()
            else:
                raise forms.ValidationError(
                    'The email address entered is already registered.'
                )
        return email
