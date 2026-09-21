import os
import sys

from django.core.management import execute_from_command_line


def radioco_admin():
    os.environ["DJANGO_SETTINGS_MODULE"] = "radioco.settings"

    execute_from_command_line(sys.argv)
