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


from radioco.schedules.models import Schedule, Slot
from django.contrib import admin


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'runtime')
    list_filter = ('programme__name', 'runtime')

    def name(self, slot):
        return slot.programme.name
    name.admin_order_field = 'programme__name'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    change_list_template = "admin/schedules/calendar.html"

    def has_add_permission(self, request):
        return False
