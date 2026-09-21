import datetime
from typing import ClassVar

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0009_programme_remove_dates"),
    ]

    operations: ClassVar = [
        migrations.AddField(
            model_name="programme",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    1980, 1, 1, 0, 0, 0, tzinfo=timezone.get_default_timezone()
                ),
                auto_now_add=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="programme",
            name="updated_at",
            field=models.DateTimeField(default=timezone.now(), auto_now=True),
            preserve_default=False,
        ),
    ]
