from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView

from .forms import PartnerCampaignCreateForm, PartnerCampaignLookupForm
from .models import PartnerCampaign


class PartnerCampaignCreateView(CreateView):
    model = PartnerCampaign
    form_class = PartnerCampaignCreateForm
    template_name = 'partners/partnercampaign_form.html'

    def get_success_url(self):
        return reverse('partner_campaign_thanks', kwargs={'pk': self.object.pk})


class PartnerCampaignThanksView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_thanks.html'


class PartnerCampaignLookupFormView(FormView):
    form_class = PartnerCampaignLookupForm
    template_name = 'partners/partnercampaign_lookup.html'

    def form_valid(self, form):
        partner_key = form.cleaned_data.get('partner_key')
        email = form.cleaned_data.get('email')
        try:
            partner_campaign = PartnerCampaign.objects.get(
                key_string=partner_key, email=email
            )
            return redirect('partner_campaign_detail', pk=partner_campaign.pk)
        except PartnerCampaign.DoesNotExist:
            form.add_error(None, 'No matching partner campaign found.')
            return self.form_invalid(form)


class PartnerCampaignDetailView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['object'].contacts.count()
        return context
