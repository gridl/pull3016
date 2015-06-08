"""pull3016 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.db import transaction
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


admin.autodiscover()


class NonAtomicAPIExceptionView(APIView):
    @method_decorator(transaction.non_atomic_requests)
    def dispatch(self, *args, **kwargs):
        return super(NonAtomicAPIExceptionView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        get_user_model().objects.all()
        raise Http404


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', NonAtomicAPIExceptionView.as_view())
]
