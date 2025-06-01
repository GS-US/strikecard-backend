from django import forms

from regions.models import Zip

from .models import PendingContact


class PendingContactForm(forms.ModelForm):
    email = forms.CharField(required=True)
    zip_code = forms.CharField(label='ZIP Code', max_length=5)
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

    def clean_zip_code(self):
        zip_code_input = self.cleaned_data.get('zip_code').strip()
        try:
            zip_instance = Zip.objects.get(code=zip_code_input)
        except Zip.DoesNotExist:
            raise forms.ValidationError('Enter a valid zip code')
        return zip_instance
