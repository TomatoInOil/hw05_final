from django.conf import settings
from django.urls import path

from . import views

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('403/', views.csrf_failure)
    ]
