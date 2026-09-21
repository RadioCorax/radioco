from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0007_change_default_image"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="programme",
            name="language",
            field=models.CharField(
                default=b"es",
                max_length=7,
                verbose_name="language",
                choices=[(b"es", "Spanish"), (b"en", "English"), (b"gl", "Galician")],
            ),
        ),
    ]
