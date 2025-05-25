from django.urls import reverse
from django.views.generic.edit import FormView

from contacts.forms import PendingContactForm


class IndexView(FormView):
    template_name = 'index.html'
    form_class = PendingContactForm

    def get_initial(self):
        initial = super().get_initial()
        partner_key = self.request.GET.get('partner_key')
        if partner_key:
            initial['partner_key'] = partner_key
        return initial
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pending_contact_detail', kwargs={'pk': self.object.pk})
