from typing import ClassVar

from django.db import migrations


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0014_alter_unique_episode"),
        ("schedules", "0007_migrate_schedules_to_slots"),
    ]

    operations: ClassVar = [
        migrations.RemoveField(
            model_name="programme",
            name="_runtime",
        ),
    ]
