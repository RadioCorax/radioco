from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("schedules", "0003_add_schedule_board_slug"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="scheduleboard",
            name="slug",
            field=models.SlugField(unique=True, max_length=255),
        ),
    ]
