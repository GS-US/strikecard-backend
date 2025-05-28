from django.urls import path
from .views import PartnerCampaignCreateView, PartnerCampaignThanksView, PartnerCampaignLookupView

urlpatterns = [
    path('create/', PartnerCampaignCreateView.as_view(), name='partner_campaign_create'),
    path('thanks/<int:pk>/', PartnerCampaignThanksView.as_view(), name='partner_campaign_thanks'),
    path(
        'lookup/',
        PartnerCampaignLookupView.as_view(),
        name='partner_campaign_lookup',
    ),
    path(
        'lookup/<int:pk>/',
        PartnerCampaignLookupView.as_view(),
        name='partner_campaign_detail',
    ),
]
