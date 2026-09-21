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

from django.shortcuts import render

from radioco.global_settings.models import CalendarConfiguration


def schedule_list(request):
    calendar_configuration = CalendarConfiguration.objects.get()
    context = {
        'scroll_time': calendar_configuration.scroll_time.strftime('%H:%M:%S'),
        'min_time': calendar_configuration.min_time.strftime('%H:%M:%S'),
        'max_time': calendar_configuration.max_time.strftime('%H:%M:%S'),
        'first_day': calendar_configuration.first_day + 1,
        'language': request.LANGUAGE_CODE,
    }
    return render(request, 'schedules/schedules_list.html', context)
