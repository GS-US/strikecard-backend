from django.urls import path

from .views import (
    PartnerCampaignContactExportView,
    PartnerCampaignCreateView,
    PartnerCampaignDetailView,
    PartnerCampaignLookupFormView,
    PartnerCampaignThanksView,
)

urlpatterns = [
    path(
        'create/', PartnerCampaignCreateView.as_view(), name='partner_campaign_create'
    ),
    path(
        'thanks/<int:pk>/',
        PartnerCampaignThanksView.as_view(),
        name='partner_campaign_thanks',
    ),
    path(
        'lookup/',
        PartnerCampaignLookupFormView.as_view(),
        name='partner_campaign_lookup',
    ),
    path(
        'detail/<int:pk>/',
        PartnerCampaignDetailView.as_view(),
        name='partner_campaign_detail',
    ),
    path(
        'export/<int:pk>/',
        PartnerCampaignContactExportView.as_view(),
        name='partner_campaign_export',
    ),
]
