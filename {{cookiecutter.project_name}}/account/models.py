# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from lib.rest_framework_helper.common import gen_random_str


class User(AbstractUser):
    api_secret = models.CharField(
        u'Api Secret', max_length=64, null=True, blank=True)

    def generate_api_secret(self):
        if self.api_secret:
            return
        self.api_secret = gen_random_str(32, ascii_uppercase=True)
        self.save()
