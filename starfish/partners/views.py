from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import PartnerCampaignForm
from .models import PartnerCampaign

class PartnerCampaignCreateView(CreateView):
    model = PartnerCampaign
    form_class = PartnerCampaignForm
    template_name = 'partners/partnercampaign_form.html'
    def get_success_url(self):
        return reverse('partner_campaign_thanks', kwargs={'pk': self.object.pk})

class PartnerCampaignThanksView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_thanks.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
