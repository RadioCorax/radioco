# Radioco - Broadcasting Radio Recording Scheduling system.
# Copyright (C) 2014  Stefan Walluhn
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

from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from radioco.api import serializers
from radioco.schedules.models import Transmission
from radioco.test.utils import TestDataMixin, now


class TestSerializers(TestDataMixin, TestCase):
    def test_programme(self):
        serializer = serializers.ProgrammeSerializer(
            self.programme, context={'request': None})
        self.assertListEqual(
            list(serializer.data.keys()),
            [
                'name', 'synopsis', 'photo', 'language', 'website', 'category',
                'created_at', 'updated_at', 'url'])

    def test_programme_photo_url(self):
        serializer = serializers.ProgrammeSerializer(
            self.programme, context={'request': None})
        self.assertEqual(
            serializer.data['photo'], "/media/defaults/example/radio_5.jpg")

    def test_slot(self):
        serializer = serializers.SlotSerializer(
            self.slot, context={'request': None})
        self.assertDictEqual(serializer.data, dict(
            name=u'Classic hits (1:00:00)',
            runtime='01:00:00',
            programme=u'/api/2/programmes/classic-hits',
            url=u'/api/2/slots/5'))

    def test_episode(self):
        serializer = serializers.EpisodeSerializer(
            self.episode, context={'request': None})
        self.assertListEqual(
            list(serializer.data.keys()),
            [
                'programme', 'title', 'summary', 'issue_date', 'season',
                'number_in_season', 'created_at', 'updated_at', 'url'])

    def test_episode_programme(self):
        serializer = serializers.EpisodeSerializer(
            self.episode, context={'request': None})
        self.assertEqual(
            serializer.data['programme'], u'/api/2/programmes/classic-hits')

    def test_schedule(self):
        serializer = serializers.ScheduleSerializer(
            self.schedule, context={'request': None})
        self.assertDictEqual(serializer.data, dict(
            type='L', id=6,
            slot=u'/api/2/slots/5',
            title=u'Classic hits',
            source=None,
            start='2015-01-01T14:00:00+01:00',
            end='2015-01-01T15:00:00+01:00'))

    def test_transmission(self):
        serializer = serializers.TransmissionSerializer(
            Transmission(
                self.schedule,
                timezone.make_aware(datetime.datetime(2015, 1, 6, 14, 0, 0))),
            context={'request': None})
        data = serializer.data

        self.assertListEqual(
            list(data.keys()),
            ['start', 'end', 'type', 'programme', 'episode', 'schedule'])

        self.assertEqual(data['start'], '2015-01-06T14:00:00+01:00')
        self.assertEqual(data['programme']['name'], u'Classic hits')
        self.assertEqual(data['episode']['title'], u'Episode 1')
        self.assertEqual(data['type'], u'L')
        self.assertEqual(data['schedule'], 6)


class TestAPI(TestDataMixin, APITestCase):
    def setUp(self):
        admin = User.objects.create_user(
            username='klaus', password='topsecret')
        admin.user_permissions.add(
            Permission.objects.get(codename='add_schedule'))
        admin.user_permissions.add(
            Permission.objects.get(codename='change_schedule'))

        User.objects.create_user(username='someone', password='topsecret')

    def test_api(self):
        response = self.client.get('/api/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_programmes_get_all(self):
        response = self.client.get('/api/2/programmes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_programmes_post(self):
        response = self.client.post('/api/2/programmes')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_programmes_put(self):
        response = self.client.put('/api/2/programmes')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_programmes_delete(self):
        response = self.client.delete('/api/2/programmes')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_slots_get_all(self):
        response = self.client.get('/api/2/slots')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_slots_post(self):
        response = self.client.post('/api/2/slots')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_episodes_get_all(self):
        response = self.client.get('/api/2/episodes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_episodes_post(self):
        response = self.client.post('/api/2/episodes')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_episodes_put(self):
        response = self.client.put('/api/2/episodes')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_episodes_delete(self):
        response = self.client.delete('/api/2/episodes')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_schedules_get_all(self):
        response = self.client.get('/api/2/schedules')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_schedules_post_unauthenticated(self):
        response = self.client.post('/api/2/schedules')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_schedules_post_authenticated_no_permission(self):
        self.client.login(username="someone", password="topsecret")
        response = self.client.post('/api/2/schedules')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_schedules_post(self):
        self.client.login(username="klaus", password="topsecret")
        response = self.client.post('/api/2/schedules', dict(
            slot='http://127.0.0.1:8000/api/2/slots/5',
            start='2017-12-26T03:00:00',
            type='L'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_schedules_patch(self):
        self.client.login(username="klaus", password="topsecret")
        response = self.client.patch('/api/2/schedules/1', dict(
            start='2017-12-26T03:00:00', type='L'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch(
        'django.utils.timezone.now',
        lambda: timezone.make_aware(datetime.datetime(2015, 1, 6, 14, 30, 0)))
    def test_transmissions(self):
        response = self.client.get('/api/2/transmissions')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 20)

    def test_transmission_after(self):
        response = self.client.get(
            '/api/2/transmissions',
            {'after': datetime.datetime(2015, 2, 1, 7, 0).isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            sorted(response.data, key=lambda t: t['start'])[0]['start'],
            '2015-02-01T08:00:00+01:00')

    @mock.patch('django.utils.timezone.now', now)
    def test_transmission_before(self):
        response = self.client.get(
            '/api/2/transmissions',
            {'before': datetime.datetime(2015, 1, 14, 21, 0).isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            sorted(response.data, key=lambda t: t['start'])[-1]['start'],
            '2015-01-14T20:00:00+01:00')

    def test_transmission_before_earlier_than_after(self):
        with self.assertRaises(ValidationError):
            self.client.get(
                '/api/2/transmissions',
                dict(
                    after=datetime.datetime(2015, 2, 14, 21, 0).isoformat(),
                    before=datetime.datetime(2015, 1, 14, 21, 0).isoformat()))

    def test_transmission_invalid_input(self):
        with self.assertRaises(ValidationError):
            self.client.get('/api/2/transmissions',
                            {'after': 'invalid date format'})

    @mock.patch(
        'django.utils.timezone.now',
        lambda: timezone.make_aware(datetime.datetime(2015, 1, 6, 14, 30, 0)))
    def test_transmission_now(self):
        response = self.client.get('/api/2/transmissions/now')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            [(t['programme']['name'], t['start']) for t in response.data],
            [(u'Classic hits', '2015-01-06T14:00:00+01:00')])
