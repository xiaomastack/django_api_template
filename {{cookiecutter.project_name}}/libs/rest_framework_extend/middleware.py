# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.deprecation import MiddlewareMixin
import logging
import json


class ApiLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.apiLogger = logging.getLogger('api')

    def __call__(self, request):
        try:
            body = json.loads(request.body)
        except Exception:
            body = dict()
        body.update(dict(request.POST))
        if 'password' in body.keys():
            del body['password']
        response = self.get_response(request)
        if request.method not in ('GET', 'HEAD'):
            self.apiLogger.info("{} {} {} {} {} {}".format(
                request.user, request.method, request.path, body,
                response.status_code, response.reason_phrase))
        return response
