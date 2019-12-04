"""{{cookiecutter.project_name}} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api import hs
from lib.rest_framework_extend.token import ObtainExpiringAuthToken
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='{{cookiecutter.project_name}} API')

urlpatterns = [
    url(r'^hs/', hs),
    url(r'^docs/', schema_view, name='docs'),
    url(r'^admin/', admin.site.urls),
    url(r'^token/', ObtainExpiringAuthToken.as_view(), name='auth_token'),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
