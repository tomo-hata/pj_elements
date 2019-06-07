# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from datetime import datetime
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.shortcuts import redirect
from . import forms, models


def hello_world(request):
    return HttpResponse('Hello World!')

def hello_template(request):
    d = {
        'hour': datetime.now().hour,
        'message': 'Sample message',
    }
    return render(request, 'index.html', d)

def hello_if(request):
    d = {
        'is_visible': False,
        'empty_str': '',
    }
    return render(request, 'if.html', d)

# elements
def issueasset(request):
    d = {
        'assetamount': request.GET.get('assetamount'),
        'tokenamount': request.GET.get('tokenamount')
    }

    #return render(request, 'models.html', d)
    return render(request, 'issueasset.html', d)

def hello_models(request):
    form = forms.HelloForm(request.POST or None)
    if form.is_valid():
        models.Hello.objects.create(**form.cleaned_data)
        return redirect('elements:hello_models')

    d = {
        'form': form,
        'hello_qs': models.Hello.objects.all().order_by('-id')
    }
    return render(request, 'models.html', d)

def hello_forms(request):
    form = forms.HelloForm(request.GET or None)
    if form.is_valid():
        message = 'データ検証に成功しました'
    else:
        message = 'データ検証に失敗しました'
    d = {
        'form': form,
        'message': message,
    }
    return render(request, 'forms.html', d)


from django.shortcuts import redirect
from . import forms, models

def elements_models(request):
    form = forms.IssueAssetForm(request.POST or None)
    if form.is_valid():
        models.IssueAsset.objects.create(**form.cleaned_data)
        return redirect('elements:elements_models')

    d = {
        'form': form,
        'hello_qs': models.IssueAsset.objects.all().order_by('-id')
    }
    return render(request, 'models.html', d)
