# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-17 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160104_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='defaults/default-userprofile-avatar.jpg', upload_to='avatars/', verbose_name='avatar'),
        ),
    ]
