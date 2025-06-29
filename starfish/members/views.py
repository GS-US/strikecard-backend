from chapters.models import Chapter
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from .forms import PendingMemberForm
from .models import PendingMember


def validate_member(request, token):
    pending_member = get_object_or_404(PendingMember, validation_token=token)
    member = pending_member.validate_member()
    if member:
        return redirect('validation_success', slug=member.chapter.slug)
    else:
        return redirect('validation_failed')


class PendingMemberDetailView(DetailView):
    model = PendingMember

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validation_link'] = context['object'].get_validation_link(self.request)
        return context


class PendingMemberCreateView(CreateView):
    model = PendingMember
    form_class = PendingMemberForm
    template_name = 'members/pendingmember_form.html'

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
        return reverse('pending_member_detail', kwargs={'pk': self.object.pk})


class SuccessView(DetailView):
    model = Chapter
    template_name = 'members/validation_success.html'
    slug_url_kwarg = 'slug'
