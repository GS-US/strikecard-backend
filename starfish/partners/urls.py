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
        'thanks/<slug:slug>/',
        PartnerCampaignThanksView.as_view(),
        name='partner_campaign_thanks',
    ),
    path(
        'lookup/',
        PartnerCampaignLookupFormView.as_view(),
        name='partner_campaign_lookup',
    ),
    path(
        '<slug:slug>/',
        PartnerCampaignDetailView.as_view(),
        name='partner_campaign_detail',
    ),
    path(
        '<slug:slug>/export/',
        PartnerCampaignContactExportView.as_view(),
        name='partner_campaign_export',
    ),
]
