"""Main URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
import learn


urlpatterns = [
    url(r'^learn/', include('learn.urls')),
    url(r'^rest-framework-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^($|about|task)', learn.views.frontend_app, name='frontend_app'),
]
