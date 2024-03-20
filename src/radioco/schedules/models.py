# Radioco - Broadcasting Radio Recording Scheduling system.
# Copyright (C) 2014  Iago Veloso Abalo, Stefan Walluhn
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


from django.db import models
from django.utils.translation import gettext_lazy as _

from radioco.programmes.models import Episode, Programme
from radioco.schedules.wrapper import RecurrenceFieldWrapper


class Slot(models.Model):
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, verbose_name=_("programme"))
    runtime = models.DurationField(
        verbose_name=_("runtime"), help_text=_("runtime in seconds"))

    class Meta:
        ordering = ["programme__name"]

    def __str__(self):
        return "{:s} ({:s})".format(self.programme.name, str(self.runtime))


class Schedule(models.Model):
    LIVE = 'L'
    BROADCAST = 'B'
    BROADCAST_SYNDICATION = 'S'
    REPETITION = 'R'
    SCHEDULE_TYPE = (
        (LIVE, _("live")),
        (BROADCAST, _("broadcast")),
        (BROADCAST_SYNDICATION, _("broadcast syndication")),
        (REPETITION, _("repetition")))

    class Meta:
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')

    slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, verbose_name=_("slot"))
    type = models.CharField(
        verbose_name=_("type"), choices=SCHEDULE_TYPE, max_length=1)
    recurrences = RecurrenceFieldWrapper(verbose_name=_("recurrences"))
    source = models.ForeignKey(
        'self', blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("source"),
        help_text=_("It is used when is a broadcast."))

    @property
    def runtime(self):
        return self.slot.runtime

    @property
    def start(self):
        return self.recurrences.dtstart

    @start.setter
    def start(self, start_date):
        self.recurrences.dtstart = start_date

    @property
    def end(self):
        if not self.start:
            return None
        return self.start + self.runtime

    def dates_between(self, after, before):
        """
            Return a sorted list of dates between after and before
        """
        return self.recurrences.between(after, before, inc=True)

    def date_before(self, before):
        return self.recurrences.before(before, inc=True)

    def date_after(self, after, inc=True):
        return self.recurrences.after(after, inc=inc)

    def __str__(self):
        return ' - '.join(
            [self.start.strftime('%A'), self.start.strftime('%X')])


class Transmission(object):
    @classmethod
    def at(cls, at):
        schedules = Schedule.objects.all()
        for schedule in schedules:
            date = schedule.date_before(at)
            if date is None:
                continue
            if at < date + schedule.runtime:
                yield cls(schedule, date)

    @classmethod
    def between(cls, after, before, schedules=None):
        if schedules is None:
            schedules = Schedule.objects.all()

        for schedule in schedules:
            for date in schedule.dates_between(after, before):
                yield cls(schedule, date)

    def __init__(self, schedule, date):
        if not (schedule.date_before(date) == date):
            raise ValueError("no scheduled transmission on given date")

        # we need to track the schedule id for admin calendar
        self.schedule = schedule

        self.programme = schedule.slot.programme
        self.type = schedule.type
        self.start = date
        self.end = date + schedule.slot.runtime

        self.episode = self._get_or_create_episode()

    def _get_or_create_episode(self):
        try:
            if self.type == Schedule.REPETITION:
                _episodes = Episode.objects.filter(
                    programme=self.programme,
                    issue_date__lt=self.start)
                return _episodes.latest('issue_date')

            return Episode.objects.get(
                programme=self.programme, issue_date=self.start)
        except Episode.DoesNotExist:
            return None
