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


from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import gettext_lazy as _
from filebrowser.sites import site as filebrowser_site

admin.site.site_header = _('RadioCo administration')
admin.site.site_title = _('RadioCo site admin')


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('filebrowser/', filebrowser_site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('api/2/', include('radioco.api.urls', namespace="api")),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='admin_password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('', admin.site.urls),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path(r'^__debug__/', include(debug_toolbar.urls))]

# Media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static
urlpatterns += staticfiles_urlpatterns()
