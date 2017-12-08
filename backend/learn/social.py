"""Login views for social media (Facebook and Google).
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.forms import SignupForm
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from lazysignup.utils import is_lazy_user
from rest_auth.registration.views import SocialLoginView
from learn.users import convert_lazy_user


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:3000'


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:3000'


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if is_lazy_user(request.user):
            request.robomission_lazy_user = request.user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if hasattr(request, 'robomission_lazy_user'):
            lazy_user = request.robomission_lazy_user
            convert_lazy_user(lazy_user, user)
            del request.robomission_lazy_user
        return user
