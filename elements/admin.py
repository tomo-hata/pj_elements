# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from elements.models import IssueAsset 
from django.contrib import admin
 
admin.site.register(IssueAsset)
