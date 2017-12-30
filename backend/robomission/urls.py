"""Main URL Configuration
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
import learn
from learn import social


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
    url(r'^monitoring/', include('monitoring.urls')),
    url(r'^rest-framework-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', social.FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', social.GoogleLogin.as_view(), name='google_login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^($|about|task|monitoring)', learn.views.frontend_app, name='frontend_app'),
]

# Set up media serving for development.
if settings.DEVELOPMENT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
