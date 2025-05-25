from django.urls import path
from django.views.generic import TemplateView
from .views import PartnerCampaignCreateView

urlpatterns = [
    path('create/', PartnerCampaignCreateView.as_view(), name='partner_campaign_create'),
    path('thanks/', TemplateView.as_view(template_name='partners/partnercampaign_thanks.html'), name='partner_campaign_thanks'),
]
