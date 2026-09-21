from typing import ClassVar

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("users", "0001_initial"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="userprofile",
            name="bio",
            field=ckeditor.fields.RichTextField(verbose_name="biography", blank=True),
            preserve_default=True,
        ),
    ]
