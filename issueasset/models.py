# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Elements modes
class IssueAsset(models.Model):
     assetid = models.CharField(
         max_length=100,
         verbose_name='アセットID名',
     )
     txid = models.CharField(
         max_length=100,
         verbose_name='トランザクションID名',
     )
     assetamount = models.CharField(
         max_length=40,
         verbose_name='発行数量',
         help_text='アセットの発行数量を入力してください',
     )
     tokenamount = models.CharField(
         max_length=1,
         verbose_name='再発行要否（1:有、0:無）',
         help_text='再発行要否（1:再発行有、0:再発行無）を入力してください。',
     )
     created_at = models.DateTimeField(
         auto_now_add=True,
         verbose_name='登録日時',
     )

     def __str__(self):
          return self.assetid
          
          
class SendAsset(models.Model):
     assetid = models.CharField(
         max_length=100,
         verbose_name='アセットID名',
     )
     txid = models.CharField(
         max_length=100,
         verbose_name='トランザクションID名',
     )
     addresstosend = models.CharField(
         max_length=100,
         verbose_name='送金先アドレス',
     )
     amounttosend = models.CharField(
         max_length=40,
         verbose_name='送金数量',
         help_text='アセットの送金数量を入力してください',
     )
     balance = models.CharField(
         max_length=40,
         verbose_name='アセット残高',
     )
     sent_at = models.DateTimeField(
         auto_now_add=True,
         verbose_name='送金日時',
     )

     def __str__(self):
          return self.txid



