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


from typing import ClassVar

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.translation import gettext as _

from radioco.global_settings.models import (
    CalendarConfiguration,
    PodcastConfiguration,
    SiteConfiguration,
)

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_str as force_unicode


@admin.register(CalendarConfiguration, SiteConfiguration)
class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        url_name_prefix = f"{self.model._meta.app_label}_{self.model._meta.model_name}"
        custom_urls = [
            path(
                "history/",
                self.admin_site.admin_view(self.history_view),
                {"object_id": "1"},
                name=f"{url_name_prefix}_history",
            ),
            path(
                "",
                self.admin_site.admin_view(self.change_view),
                {"object_id": "1"},
                name=f"{url_name_prefix}_change",
            ),
        ]
        # By inserting the custom URLs first, we overwrite the standard URLs.
        return custom_urls + urls

    def response_change(self, request, obj):
        msg = _("%(obj)s was changed successfully.") % {"obj": force_unicode(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect("../../")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if object_id == "1":
            self.model.objects.get_or_create(pk=1)
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )


@admin.register(PodcastConfiguration)
class PodcastConfigurationAdmin(SingletonModelAdmin):
    readonly_fields: ClassVar = ["recorder_token"]
