from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from partners.models import PartnerCampaign

from chapters.models import Chapter, ChapterRole

from .forms import PendingContactForm
from .models import Contact, PendingContact


def validate_contact(request, token):
    pending_contact = get_object_or_404(PendingContact, validation_token=token)
    contact = pending_contact.validate_contact()
    if contact:
        return redirect('validation_success', slug=contact.chapter.slug)
    else:
        return redirect('validation_failed')


class PendingContactDetailView(DetailView):
    model = PendingContact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validation_link'] = context['object'].get_validation_link(self.request)
        return context


class PendingContactCreateView(CreateView):
    model = PendingContact
    form_class = PendingContactForm
    template_name = 'contacts/pendingcontact_form.html'

    def form_valid(self, form):
        partner_key = form.cleaned_data.get('partner_key')
        if partner_key:
            try:
                partner_campaign = PartnerCampaign.objects.get(key_string=partner_key)
                form.instance.partner_campaign = partner_campaign
            except PartnerCampaign.DoesNotExist:
                pass  # Optionally handle invalid partner_key
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pending_contact_detail', kwargs={'pk': self.object.pk})


class SuccessView(DetailView):
    model = Chapter
    template_name = 'contacts/validation_success.html'
    slug_url_kw_arg = 'slug'
