from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('foo/bar/', admin.site.urls),
]
