from django.urls import path
from .views import PartnerCampaignCreateView, PartnerCampaignThanksView

urlpatterns = [
    path('create/', PartnerCampaignCreateView.as_view(), name='partner_campaign_create'),
    path('thanks/<int:pk>/', PartnerCampaignThanksView.as_view(), name='partner_campaign_thanks'),
]
