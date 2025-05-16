from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from .models import PendingContact, Contact
from .forms import PendingContactForm

from chapters.models import ChapterRole
from rules.contrib.views import PermissionRequiredMixin

from django.urls import reverse

def validate_contact(request, token):
    pending_contact = get_object_or_404(PendingContact, validation_token=token)
    if not pending_contact.token_is_expired():
        contact = Contact.objects.create(
            name=pending_contact.name,
            email=pending_contact.email,
            phone=pending_contact.phone,
            zip_code=pending_contact.zip_code,
            chapter=pending_contact.chapter,
            partner_campaign=pending_contact.partner_campaign,
        )
        pending_contact.delete()
        return redirect('validation_success')
    else:
        return redirect('validation_failed')


class PendingContactCreateView(CreateView):
    model = PendingContact
    form_class = PendingContactForm
    template_name = 'contacts/pending_contact_form.html'
    success_url = reverse_lazy('pending_contact_thank_you')

    def form_valid(self, form):
        self.object = form.save()
        self.object.send_validation_email(self.request)
        return super().form_valid(form)


class ContactListView(PermissionRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    permission_required = 'contacts.view_contact'

    def get_queryset(self):
        qs = super().get_queryset()
        user_chapters = ChapterRole.objects.filter(user=self.request.user).values_list(
            'chapter', flat=True
        )
        return qs.filter(chapter__in=user_chapters)


class ContactCreateView(PermissionRequiredMixin, CreateView):
    model = Contact
    fields = ['name', 'email', 'phone', 'zip_code', 'chapter', 'partner_campaign']
    template_name = 'contacts/contact_form.html'
    permission_required = 'contacts.add_contact'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_chapters = ChapterRole.objects.filter(user=self.request.user).values_list(
            'chapter', flat=True
        )
        form.fields['chapter'].queryset = Chapter.objects.filter(id__in=user_chapters)
        return form


class ContactUpdateView(PermissionRequiredMixin, UpdateView):
    model = Contact
    fields = ['name', 'email', 'phone', 'zip_code']
    template_name = 'contacts/contact_form.html'
    permission_required = 'contacts.change_contact'

    def get_permission_object(self):
        return self.get_object()


class ContactDeleteView(PermissionRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    permission_required = 'contacts.delete_contact'

    def get_permission_object(self):
        return self.get_object()
