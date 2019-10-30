# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import ugettext_lazy as _


class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Internal server error.')
    default_code = 'internal_server_error'
