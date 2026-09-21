from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("global_settings", "0002_remove_calendarconfiguration_display_next_weeks"),
    ]

    operations: ClassVar = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="footer",
            field=models.TextField(
                default=b"",
                help_text="Can contain raw HTML.",
                verbose_name="Footer",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
