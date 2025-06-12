from contacts.admin import ContactResource
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, View

from .forms import PartnerCampaignCreateForm, PartnerCampaignLookupForm
from .models import PartnerCampaign


class PartnerCampaignCreateView(CreateView):
    model = PartnerCampaign
    form_class = PartnerCampaignCreateForm
    template_name = 'partners/partnercampaign_form.html'

    def get_success_url(self):
        return reverse('partner_campaign_thanks', kwargs={'slug': self.object.slug})


class PartnerCampaignThanksView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_thanks.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class PartnerCampaignLookupFormView(FormView):
    form_class = PartnerCampaignLookupForm
    template_name = 'partners/partnercampaign_lookup.html'

    def form_valid(self, form):
        slug = form.cleaned_data.get('slug')
        email = form.cleaned_data.get('email')
        try:
            partner_campaign = PartnerCampaign.objects.get(slug=slug, email=email)
            return redirect('partner_campaign_detail', slug=partner_campaign.slug)
        except PartnerCampaign.DoesNotExist:
            form.add_error(None, 'No matching partner campaign found.')
            return self.form_invalid(form)


class PartnerCampaignDetailView(DetailView):
    model = PartnerCampaign
    template_name = 'partners/partnercampaign_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['object'].contacts.count()
        context['export_url'] = reverse(
            'partner_campaign_export', kwargs={'slug': self.object.slug}
        )
        return context


class PartnerCampaignContactExportView(View):
    def get(self, request, slug):
        partner_campaign = get_object_or_404(PartnerCampaign, slug=slug)
        contacts = partner_campaign.contacts.all()

        dataset = ContactResource().export(contacts)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = (
            f'attachment; filename="contacts_{partner_campaign.slug}.csv"'
        )
        return response
