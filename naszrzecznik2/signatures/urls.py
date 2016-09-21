# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(),
        name="home"),
    url(_(r'^signatures-(?P<slug>[\w-]+)$'), views.SignatureListView.as_view(),
        name="list"),
    url(_(r'^text-(?P<slug>[\w-]+)$'), views.PetitionDetailView.as_view(),
        name="text"),
    url(_(r'^form-(?P<slug>[\w-]+)$'), views.FormView.as_view(),
        name="form"),
    url(_(r'^form-(?P<slug>[\w-]+)/thanks$'), views.ThanksView.as_view(),
        name="thanks"),
    url(r'^(?P<category_slug>[\w-]+)$', views.CategoryView.as_view(),
        name="category"),
]
