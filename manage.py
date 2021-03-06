#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.join(os.path.realpath(os.path.dirname(__file__)), 'radioco/'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "radioco.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
