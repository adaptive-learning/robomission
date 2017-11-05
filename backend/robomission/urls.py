"""Main URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
import learn


urlpatterns = [
    # Top-level public assets (such as favicon.ico and robots.txt) starts in
    # frontend public directory, then arecopied into frontend build directory,
    # and then copied into backend static directory, under `public` namespace.
    # To make sure they work (even during development, although that is not
    # necessary), redirects are created to them. In production, nginx should be
    # configured to directly access these files (for performance reasons).
    url(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('public/favicon.ico'),
            permanent=False),
        name='favicon.ico'),
    url(r'^robots.txt$',
        RedirectView.as_view(
            url=staticfiles_storage.url('public/robots.txt'),
            permanent=False),
        name='robots.txt'),

    url(r'^learn/', include('learn.urls')),
    url(r'^rest-framework-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^($|about|task)', learn.views.frontend_app, name='frontend_app'),
]
