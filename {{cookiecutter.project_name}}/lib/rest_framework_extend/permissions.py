# -*- coding: utf-8 -*-
from rest_framework import permissions


class CreatorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.creator == request.user
