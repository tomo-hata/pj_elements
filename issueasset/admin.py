# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from .models import User

#admin.site.register(User, UserAdmin)


from .models import IssueAsset,SendAsset
admin.site.register(IssueAsset)
admin.site.register(SendAsset)