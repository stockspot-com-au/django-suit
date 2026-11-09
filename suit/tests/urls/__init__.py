from django.contrib import admin
from django.urls import path

from suit.tests.models import filters_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filters-admin/', filters_site.urls),
]
