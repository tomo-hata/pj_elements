# -*- coding: utf-8 -*-

from django import forms


class HelloForm(forms.Form):
    your_name = forms.CharField(
        label='名前',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )

class IssueAssetForm(forms.Form):
    assetamount = forms.CharField(
        label='発行数量',
        max_length=30,
        required=True,
        widget=forms.TextInput()
    )
