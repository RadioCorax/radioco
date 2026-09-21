# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0004_unique_schedule_board_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='schedule_board',
        ),
        migrations.DeleteModel(
            name='ScheduleBoard',
        ),
    ]
