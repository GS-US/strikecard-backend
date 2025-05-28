from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView
from .forms import PartnerCampaignCreateForm, PartnerCampaignLookupForm
from .models import PartnerCampaign

class PartnerCampaignCreateView(CreateView):
    model = PartnerCampaign
    form_class = PartnerCampaignCreateForm
    template_name = 'partners/partnercampaign_form.html'

    def get_context_data(self, form=None):
        context = super().get_context_data(fom=form)
        context['lookup_form'] = PartnerCampaignLookupForm()
        return context

    def get_success_url(self):
        return reverse('partner_campaign_thanks', kwargs={'pk': self.object.pk})

class PartnerCampaignThanksView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_thanks.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class PartnerCampaignLookupView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_detail.html'

    def form_valid(self, form):
        partner_key = form.cleaned_data.get('partner_key')
        email = form.cleaned_data.get('email')
        context = self.get_context_data(form=form)
        context['object'] = PartnerCampaign.objects.get(
            key_string=partner_key, email=email
        )
        return self.render_to_response(context)
