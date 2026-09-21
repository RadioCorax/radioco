from typing import ClassVar

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations: ClassVar = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("bio", models.TextField(verbose_name="biography", blank=True)),
                (
                    "avatar",
                    models.ImageField(
                        default=b"/static/radio/images/default-userprofile-avatar.jpg",
                        upload_to=b"avatars/",
                        verbose_name="avatar",
                    ),
                ),
                (
                    "display_personal_page",
                    models.BooleanField(
                        default=False, verbose_name="display personal page"
                    ),
                ),
                ("slug", models.SlugField(max_length=30)),
                (
                    "user",
                    models.OneToOneField(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "default_permissions": ("change",),
                "verbose_name": "user profile",
                "verbose_name_plural": "user profile",
            },
            bases=(models.Model,),
        ),
    ]
