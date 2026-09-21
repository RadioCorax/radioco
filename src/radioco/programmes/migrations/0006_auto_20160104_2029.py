from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0005_auto_20150531_1734"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="programme",
            name="photo",
            field=models.ImageField(
                default=b"defaults/default-programme-photo.jpg",
                upload_to=b"photos/",
                verbose_name="photo",
            ),
        ),
    ]
