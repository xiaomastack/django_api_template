# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.response import Response
from collections import OrderedDict
import re


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        django_paginator_class = DjangoPaginator
        queryset_old = queryset
        queryset = queryset['results']
        paginator = django_paginator_class(queryset, page_size)

        page_number = request.query_params.get(self.page_query_param, 1)
        self.page = paginator.page(1)

        self.page.paginator.count = queryset_old["count"]
        url = request.build_absolute_uri()
        if queryset_old["next"]:
            if '?' not in url:
                url = url + '?page=1'
            elif 'page' not in url:
                url = url + '&page=1'
            self.page.paginator.next = re.sub('page=(\\d+)', 'page='+str(int(page_number) + 1), url)
        else:
            self.page.paginator.next = None
        if queryset_old["previous"]:
            self.page.paginator.previous = re.sub('page=(\\d+)', 'page='+str(int(page_number) - 1), url)
        else:
            self.page.paginator.previous = None

        return list(self.page)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.page.paginator.next),
            ('previous', self.page.paginator.previous),
            ('results', data)
        ]))
