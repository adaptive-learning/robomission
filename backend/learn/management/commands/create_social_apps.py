from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = "Create social apps for authentication."

    def handle(self, *args, **options):
        site = Site.objects.get_current()
        site.domain = site.name = 'robomise.cz'
        site.save()
        SocialApp.objects.all().delete()
        apps = [
            SocialApp.objects.create(
                provider='facebook',
                name='Facebook',
                client_id=settings.SOCIAL_AUTH_FACEBOOK_KEY,
                secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET),
            SocialApp.objects.create(
                provider='google',
                name='Google',
                client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET)]
        for app in apps:
            app.sites.add(site)
