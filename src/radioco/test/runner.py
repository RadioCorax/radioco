# This file mainly exists to allow python setup.py test to work.
import os
import sys
import django

from django.test.utils import get_runner
from django.conf import settings


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'radioco.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests([])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
