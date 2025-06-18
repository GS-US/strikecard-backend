from django import forms

from .models import PartnerCampaign


class PartnerCampaignCreateForm(forms.ModelForm):
    class Meta:
        model = PartnerCampaign
        fields = [
            'name',
            'email',
            'url',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name = self.fields["name"]
        name.widget = forms.TextInput(attrs={"placeholder": "e.g., Jordan Doe"})

        email = self.fields["email"]
        email.widget = forms.EmailInput(attrs={"placeholder": "e.g., j.doe@abc.com"})

        url = self.fields["url"]
        url.widget = forms.URLInput(
            attrs={"placeholder": "e.g., https://www.jdoe-campaign.com"}
        )


class PartnerCampaignLookupForm(forms.Form):
    slug = forms.CharField()
    email = forms.CharField()
