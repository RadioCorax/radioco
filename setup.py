# Radioco - Broadcasting Radio Recording Scheduling system.
# Copyright (C) 2014  Iago Veloso Abalo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

from setuptools import setup, find_packages

import radioco

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    author='Iago Veloso Abalo, Stefan Walluhn',
    author_email='author@radioco.org',
    name='radioco',
    version=radioco.__version__,
    description='This app provides an easy way to set up your radio',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/RadioCorax/radioco',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'Django==3.2',
        'Pillow',
        'django-ckeditor',
        'django-disqus',
        'django-filebrowser<4',
        'django-filter<3',
        'django-grappelli<2.16',
        'django-npm',
        'django-recurrence',
        'djangorestframework',
        'python-dateutil',
        'pytz',
    ],
    tests_require=['mock'],
    test_suite = "radioco.test.runner.runtests",
)
