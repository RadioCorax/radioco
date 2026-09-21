from typing import ClassVar

from django.db import migrations


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("global_settings", "0001_initial"),
    ]

    operations: ClassVar = [
        migrations.RemoveField(
            model_name="calendarconfiguration",
            name="display_next_weeks",
        ),
    ]
