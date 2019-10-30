# -*- coding: utf-8 -*-
import datetime
from account.models import User
from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from django.utils.translation import ugettext_lazy as _
from rest_framework_httpsignature.authentication import SignatureAuthentication


class HTTPSignatureAuthentication(SignatureAuthentication):
    API_KEY_HEADER = 'X-Api-Key'

    def fetch_user_data(self, api_key):
        try:
            # get cache
            if settings.LOCAL_CACHE:
                user = cache.get(api_key)
                if user:
                    return (user[0], user[1])
            user = User.objects.get(username=api_key, is_active=True)
            # set cache
            if settings.LOCAL_CACHE:
                cache.set(api_key, [user, user.api_secret], 60 * 60 * 24)
            return (user, user.api_secret)
        except User.DoesNotExist:
            return None


class ExpiringTokenAuthentication(TokenAuthentication):
    """Set up token expired time"""

    def authenticate_credentials(self, key):
        EXPIRE_MINUTES = getattr(settings, 'TOKEN_EXPIRE_MINUTES', 1)
        # Search token in cache
        cache_user = cache.get(key)
        if cache_user:
            return (cache_user, key)
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))
        time_now = datetime.datetime.now()
        if token.created < time_now - datetime.timedelta(
                minutes=EXPIRE_MINUTES):
            token.delete()
            raise exceptions.AuthenticationFailed(
                _('Token has expired then delete.'))
        if token:
            # Cache token
            cache.set(key, token.user, EXPIRE_MINUTES * 60)
        return (token.user, token)


class ObtainExpiringAuthToken(ObtainAuthToken):
    """Create user token"""

    def post(self, request):
        EXPIRE_MINUTES = getattr(settings, 'TOKEN_EXPIRE_MINUTES', 1)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data['user'])
            time_now = datetime.datetime.now()
            if not created and token.created < time_now - datetime.timedelta(
                    minutes=EXPIRE_MINUTES):
                token.delete()
                token = Token.objects.create(
                    user=serializer.validated_data['user'])
                token.created = time_now
                token.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
