# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^[htmlファイル名]$', views.[関数名], name='[表示名]'),
    # url(r'^$', views.index, name='index'),
    url(r'^issueasset$', views.issueasset, name='issueasset'),
    url(r'^search_issuance$', views.search_issuance, name='search_issuance'),
    url(r'^sendasset$', views.sendasset, name='sendasset'),
]
