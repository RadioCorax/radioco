from typing import ClassVar

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0011_episode_created_updated_at"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="episode",
            name="people",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL,
                verbose_name="people",
                through="programmes.Participant",
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="announcers",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL,
                verbose_name="announcers",
                through="programmes.Role",
                blank=True,
            ),
        ),
    ]
