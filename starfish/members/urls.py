from django.urls import path
from django.views.generic import TemplateView

from .views import (
    PendingMemberCreateView,
    PendingMemberDetailView,
    SuccessView,
    validate_member,
)

urlpatterns = [
    path(
        'signup/',
        PendingMemberCreateView.as_view(),
        name='pending_member_create_no_p',
    ),
    path('validate/<str:token>/', validate_member, name='validate_member'),
    path(
        'success/<str:slug>/',
        SuccessView.as_view(),
        name='validation_success',
    ),
    path(
        'failed/',
        TemplateView.as_view(template_name='members/validation_failed.html'),
        name='validation_failed',
    ),
    path(
        'member/<int:pk>/',
        PendingMemberDetailView.as_view(),
        name='pending_member_detail',
    ),
]
