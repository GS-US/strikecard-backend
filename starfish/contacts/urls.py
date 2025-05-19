from django.urls import path
from django.views.generic import TemplateView

from .views import PendingContactCreateView, PendingContactDetailView, validate_contact

urlpatterns = [
    path('signup/', PendingContactCreateView.as_view(), name='pending_contact_signup'),
    path('validate/<str:token>/', validate_contact, name='validate_contact'),
    path(
        'success/',
        TemplateView.as_view(template_name='contacts/validation_success.html'),
        name='validation_success',
    ),
    path(
        'failed/',
        TemplateView.as_view(template_name='contacts/validation_failed.html'),
        name='validation_failed',
    ),
    path(
        'contact/<int:id>/',
        PendingContactDetailView.as_view(),
        name='pending_contact_detail',
    ),
]
