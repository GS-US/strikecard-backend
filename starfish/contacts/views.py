from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from rules.contrib.views import PermissionRequiredMixin

from chapters.models import ChapterRole

from .forms import PendingContactForm
from .models import Contact, PendingContact


def validate_contact(request, token):
    pending_contact = get_object_or_404(PendingContact, validation_token=token)
    if pending_contact.validate_contact():
        return redirect('validation_success')
    else:
        return redirect('validation_failed')


class PendingContactDetailView(DetailView):
    model = PendingContact


class PendingContactCreateView(CreateView):
    model = PendingContact
    form_class = PendingContactForm
    template_name = 'contacts/pending_contact_form.html'
    success_url = reverse_lazy('pending_contact_detail')
