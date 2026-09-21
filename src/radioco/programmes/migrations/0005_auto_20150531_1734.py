from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0004_change_photo_url"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="podcast",
            name="episode",
            field=models.OneToOneField(
                to="programmes.Episode",
                on_delete=models.CASCADE,
                related_name="podcast",
                primary_key=True,
                serialize=False,
            ),
            preserve_default=True,
        ),
    ]
