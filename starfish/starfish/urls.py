from django.conf import settings  # Imported settings
from django.contrib import admin
from django.urls import include, path
from members.views import PendingMemberCreateView

from .views import GetTotalsView

urlpatterns = [
    path('', PendingMemberCreateView.as_view(), name='index'),
    path('p/<str:p>/', PendingMemberCreateView.as_view(), name='partner_signup'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('members/', include('members.urls')),
    path('chapters/', include('chapters.urls')),
    path('partners/', include('partners.urls')),
    path('api/totals/', GetTotalsView.as_view(), name='get_the_totals'),
    path('', include('django_prometheus.urls')),
]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
