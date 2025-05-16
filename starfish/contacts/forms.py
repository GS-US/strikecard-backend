from django import forms
from .models import PendingContact

class PendingContactForm(forms.ModelForm):
    class Meta:
        model = PendingContact
        fields = ['name', 'email', 'phone', 'zip_code',]
