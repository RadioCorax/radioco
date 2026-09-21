from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("programmes", "0012_auto_20171122_0911"),
    ]

    operations: ClassVar = [
        migrations.AddField(
            model_name="programme",
            name="website",
            field=models.URLField(blank=True),
        ),
    ]
