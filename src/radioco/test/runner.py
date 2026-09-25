# This file mainly exists to allow python setup.py test to work.
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

from radioco import settings as default_settings


def runtests():
    settings.configure(
        default_settings,
        TIME_ZONE="Europe/Berlin",
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["radioco"])
    sys.exit(bool(failures))
