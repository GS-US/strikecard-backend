from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from chapters.models import Chapter, ChapterRole
from partners.models import PartnerCampaign

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

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        partner_key = self.request.GET.get('partner_key')
        if partner_key:
            initial['partner_key'] = partner_key
        return initial
        self.object = form.save()
        return super().form_valid(form)

    def form_valid(self, form):
        partner_key = form.cleaned_data.get('partner_key')
        if partner_key:
            try:
                form.instance.partner_campaign = PartnerCampaign.objects.get(
                    key_string=partner_key
                )
            except PartnerCampaign.DoesNotExist:
                pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pending_contact_detail', kwargs={'pk': self.object.pk})


class SuccessView(DetailView):
    model = Chapter
    template_name = 'contacts/validation_success.html'
    slug_url_kw_arg = 'slug'
