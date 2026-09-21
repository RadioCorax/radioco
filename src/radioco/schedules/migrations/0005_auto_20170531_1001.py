from typing import ClassVar

from django.db import migrations


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("schedules", "0004_unique_schedule_board_slug"),
    ]

    operations: ClassVar = [
        migrations.RemoveField(
            model_name="schedule",
            name="schedule_board",
        ),
        migrations.DeleteModel(
            name="ScheduleBoard",
        ),
    ]
