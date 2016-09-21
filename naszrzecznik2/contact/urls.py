# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ContactView.as_view(), name="form"),
    url(r'^~success$', views.SuccessView.as_view(),
        name="success"),
]
