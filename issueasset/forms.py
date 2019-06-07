from django import forms
from .models import IssueAsset, SendAsset


class IssueAssetForm(forms.ModelForm):

    class Meta:
        model = IssueAsset
        fields = ('assetamount', 'tokenamount')
        widgets = {
            'assetamount': forms.TextInput(attrs={'size': 40}),
            'tokenamount': forms.TextInput(attrs={'size': 10}),
        }

class SearchForm(forms.ModelForm):

    class Meta:
        model = IssueAsset
        fields = ('assetid',)
        widgets = {
            'assetid': forms.TextInput(attrs={'size': 100}),
        }
        
class SendAssetForm(forms.ModelForm):

    class Meta:
        model = SendAsset
        fields = ('assetid','amounttosend','addresstosend')
        widgets = {
            'assetid': forms.TextInput(attrs={'size': 100}),
            'amounttosend': forms.TextInput(attrs={'size': 40}),
            'addresstosend': forms.TextInput(attrs={'size': 100}),
        }
