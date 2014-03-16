from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'radio.apps.dashboard.views.index', name="index"),
    url(r'^profile/$', 'radio.apps.dashboard.views.edit_profile', name="edit_profile"),
    url(r'^programmes/$', 'radio.apps.dashboard.views.programme_list', name="programme_list"),
    url(r'^programmes/create/$', 'radio.apps.dashboard.views.create_programme', name="create_programme"),
    url(r'^programmes/(?P<slug>[-\w]+)/$', 'radio.apps.dashboard.views.edit_programme', name="edit_programme"),
    url(r'^own/programmes/$', 'radio.apps.dashboard.views.my_programme_list', name="my_programme_list"),
    url(r'^own/programmes/(?P<slug>[-\w]+)/$', 'radio.apps.dashboard.views.edit_my_programme', name="edit_my_programme"),

    url(r'^schedule_editor/$', 'radio.apps.dashboard.views.full_calendar', name="schedule_editor"),
    url(r'^schedule_editor/all_events/', 'radio.apps.dashboard.views.all_events'),
    url(r'^schedule_editor/change_event', 'radio.apps.dashboard.views.change_event'),
    url(r'^schedule_editor/create_schedule', 'radio.apps.dashboard.views.create_schedule'),
    url(r'^schedule_editor/delete_schedule', 'radio.apps.dashboard.views.delete_schedule'),
    url(r'^schedule_editor/programmes', 'radio.apps.dashboard.views.programmes'),
)