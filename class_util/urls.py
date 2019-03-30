from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = [
    path('', RedirectView.as_view(url='distributions', permanent=False), name='index'),
    path('distributions/', include('distributions.urls', namespace='distributions')),
    path('api/distributions/', include('distributions.api.urls', namespace='distributions-api'))
]
