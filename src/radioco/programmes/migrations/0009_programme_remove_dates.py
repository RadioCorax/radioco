from typing import ClassVar

from django.db import migrations


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0008_auto_20160116_1509"),
    ]

    operations: ClassVar = [
        migrations.RemoveField(
            model_name="programme",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="programme",
            name="start_date",
        ),
    ]
