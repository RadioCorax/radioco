from django.conf.urls import url, include
from rest_framework import routers

from radioco.api import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'programmes', views.ProgrammeViewSet)
router.register(r'slots', views.SlotViewSet)
router.register(r'episodes', views.EpisodeViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'transmissions', views.TransmissionViewSet, base_name='transmission')

urlpatterns = router.urls

app_name = 'api'
