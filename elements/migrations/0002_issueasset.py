# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-13 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assetamount', models.CharField(max_length=30)),
                ('tokenamount', models.CharField(max_length=1)),
            ],
        ),
    ]