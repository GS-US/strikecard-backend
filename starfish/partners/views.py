from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PartnerCampaignForm
from .models import PartnerCampaign

class PartnerCampaignCreateView(CreateView):
    model = PartnerCampaign
    form_class = PartnerCampaignForm
    template_name = 'partners/partnercampaign_form.html'
    success_url = reverse_lazy('partner_campaign_thanks')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
