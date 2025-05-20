from django.urls import reverse
from django.views.generic.edit import FormView
from contacts.forms import PendingContactForm

class IndexView(FormView):
    template_name = 'index.html'
    form_class = PendingContactForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pending_contact_detail', kwargs={'pk': self.object.pk})
