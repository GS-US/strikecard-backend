from contacts.views import PendingContactCreateView
from django.conf import settings  # Imported settings
from django.contrib import admin
from django.urls import include, path

from .views import GetTotalsView

urlpatterns = [
    path('', PendingContactCreateView.as_view(), name='index'),
    path('p/<str:p>/', PendingContactCreateView.as_view(), name='partner_signup'),
    path('admin/', admin.site.urls),
    path('contacts/', include('contacts.urls')),
    path('chapters/', include('chapters.urls')),
    path('partners/', include('partners.urls')),
    path('api/totals/', GetTotalsView.as_view(), name='get_the_totals'),
]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
