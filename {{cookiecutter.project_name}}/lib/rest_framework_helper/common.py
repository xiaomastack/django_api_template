# -*- coding: utf-8 -*-
import string
import random
import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


def gen_random_str(length,
                   digits=True,
                   ascii_lowercase=True,
                   ascii_uppercase=False):
    chars = ''
    if digits:
        chars += string.digits
    if ascii_lowercase:
        chars += string.ascii_lowercase
    if ascii_uppercase:
        chars += string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(length))


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
