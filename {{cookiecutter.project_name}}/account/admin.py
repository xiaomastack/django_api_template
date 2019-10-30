# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User


class AccountUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'api_secret')
    search_fields = ('username', 'first_name', 'last_name', 'email',
                     'api_secret')


admin.site.register(User, AccountUserAdmin)
