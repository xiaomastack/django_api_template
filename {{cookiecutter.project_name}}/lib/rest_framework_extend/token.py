# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


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
