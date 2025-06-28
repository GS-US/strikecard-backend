from chapters.models import Chapter
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

# Import DRF dependencies
from rest_framework import generics

from .forms import PendingContactForm
from .models import PendingContact
from .serializers import PendingContactSerializer


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
        initial['partner_slug'] = self.kwargs.get('p')
        return initial

    def form_valid(self, form):
        form.instance.referer_full = self.request.META.get('HTTP_REFERER')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pending_contact_detail', kwargs={'pk': self.object.pk})


class SuccessView(DetailView):
    model = Chapter
    template_name = 'contacts/validation_success.html'
    slug_url_kwarg = 'slug'


class PendingContactCreateAPIView(generics.CreateAPIView):
    queryset = PendingContact.objects.all()
    serializer_class = PendingContactSerializer

    def perform_create(self, serializer):
        serializer.save(referer_full=self.request.META.get('HTTP_REFERER'))
