from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("global_settings", "0004_auto_20150606_1335"),
    ]

    operations: ClassVar = [
        migrations.RenameField(
            model_name="siteconfiguration",
            old_name="footer",
            new_name="about_footer",
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="more_about_us",
            field=models.TextField(default=b"", verbose_name="More info", blank=True),
            preserve_default=True,
        ),
    ]
