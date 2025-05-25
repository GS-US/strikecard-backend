from django import forms

from .models import PartnerCampaign


class PartnerCampaignForm(forms.ModelForm):
    class Meta:
        model = PartnerCampaign
        fields = [
            'name',
            'email',
            'url',
        ]
