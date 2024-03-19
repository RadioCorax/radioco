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

import datetime
import mock

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.utils import timezone

from radioco.programmes.models import Programme, Episode, EpisodeManager
from radioco.test.utils import TestDataMixin, now


class ProgrammeModelTests(TestCase):
    @mock.patch('django.utils.timezone.now', now)
    def setUp(self):
        self.programme = Programme.objects.create(
            name="Test programme",
            synopsis="This is a description",
            website="http://foo.example",
            current_season=1)

    def test_save_programme(self):
        self.assertEqual(
            self.programme, Programme.objects.get(id=self.programme.id))

    def test_slug(self):
        self.assertEqual(self.programme.slug, "test-programme")

    def test_website(self):
        self.assertEqual(self.programme.website, "http://foo.example")

    def test_created_at(self):
        self.assertEqual(
            self.programme.created_at,
            timezone.make_aware(datetime.datetime(2014, 1, 1, 13, 30, 0, 0)))

    def test_updated_at(self):
        self.assertEqual(
            self.programme.updated_at,
            timezone.make_aware(datetime.datetime(2014, 1, 1, 13, 30, 0, 0)))

    def test_str(self):
        self.assertEqual(str(self.programme), "Test programme")


class ProgrammeModelAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_fieldset(self):
        ma = ModelAdmin(Programme, self.site)
        self.assertEqual(ma.get_fields(None), [
            'name', 'synopsis', 'photo', 'language', 'current_season',
            'category', 'website', 'slug'])


class EpisodeManagerTests(TestDataMixin, TestCase):
    def setUp(self):
        self.manager = EpisodeManager()

        self.episode = self.manager.create_episode(
            timezone.make_aware(datetime.datetime(2014, 6, 14, 10, 0, 0)),
            self.programme)

    def test_create_episode(self):
        self.assertIsInstance(self.episode, Episode)

    def test_season(self):
        self.assertEqual(self.episode.season, self.programme.current_season)

    def test_number_in_season(self):
        self.assertEqual(self.episode.number_in_season, 6)

    def test_issue_date(self):
        self.assertEqual(
            self.episode.issue_date,
            timezone.make_aware(datetime.datetime(2014, 6, 14, 10, 0, 0)))

    def test_people(self):
        self.assertQuerysetEqual(
            self.episode.people.all(), self.programme.announcers.all())

    def test_last(self):
        episode = self.manager.last(self.programme)
        self.assertEqual(episode.season, 7)
        self.assertEqual(episode.number_in_season, 6)

    def test_last_none(self):
        episode = self.manager.last(Programme())
        self.assertIsNone(episode)

    def test_unfinished(self):
        episodes = self.manager.unfinished(
            self.programme, timezone.make_aware(datetime.datetime(2015, 1, 1)))
        self.assertEqual(
            next(episodes).issue_date,
            timezone.make_aware(datetime.datetime(2015, 1, 1, 14, 0)))

    def test_unfinished_none(self):
        episodes = self.manager.unfinished(Programme())
        with self.assertRaises(StopIteration):
            next(episodes)


class EpisodeModelTests(TestCase):

    @mock.patch('django.utils.timezone.now', now)
    def setUp(self):
        self.programme = Programme.objects.create(
            name="Test programme",
            synopsis="This is a description",
            current_season=8)

        self.episode = Episode.objects.create_episode(
            timezone.make_aware(datetime.datetime(2014, 1, 14, 10, 0, 0)),
            programme=self.programme)

    def test_model_manager(self):
        self.assertIsInstance(self.episode, Episode)

    def test_programme(self):
        self.assertEqual(self.episode.programme, self.programme)

    def test_created_at(self):
        self.assertEqual(
            self.episode.created_at,
            timezone.make_aware(datetime.datetime(2014, 1, 1, 13, 30, 0, 0)))

    def test_updated_at(self):
        self.assertEqual(
            self.episode.updated_at,
            timezone.make_aware(datetime.datetime(2014, 1, 1, 13, 30, 0, 0)))

    def test_str(self):
        self.assertEqual(str(self.episode), "8x1 Test programme")
