from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('programmes', '0014_alter_unique_episode'),
        ('schedules', '0007_migrate_schedules_to_slots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programme',
            name='_runtime',
        ),
    ]
