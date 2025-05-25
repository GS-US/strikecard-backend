from django import forms

from regions.models import Zip

from .models import PendingContact


class PendingContactForm(forms.ModelForm):
    email = forms.CharField(required=True)
    zip_code = forms.CharField(max_length=5)

    class Meta:
        model = PendingContact
        fields = [
            'name',
            'email',
            'phone',
            'zip_code',
        ]

    def clean_zip_code(self):
        zip_code_input = self.cleaned_data.get('zip_code').strip()
        try:
            zip_instance = Zip.objects.get(code=zip_code_input)
        except Zip.DoesNotExist:
            raise forms.ValidationError('Enter a valid zip code')
        return zip_instance
