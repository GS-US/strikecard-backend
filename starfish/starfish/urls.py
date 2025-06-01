from django.conf import settings  # Imported settings
from django.contrib import admin
from django.urls import include, path

from contacts.views import PendingContactCreateView

urlpatterns = [
    path('', PendingContactCreateView.as_view(), name='index'),
    path('p/<str:p>/', PendingContactCreateView.as_view(), name='partner_signup'),
    path('admin/', admin.site.urls),
    path('contacts/', include('contacts.urls')),
    path('chapters/', include('chapters.urls')),
    path('partners/', include('partners.urls')),
]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
