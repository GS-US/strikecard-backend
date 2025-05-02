from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from chapters.models import ChapterRole
from rules.contrib.views import PermissionRequiredMixin

from .models import Contact


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
