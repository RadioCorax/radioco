from rest_framework import routers

from radioco.api import views
from radioco.api.apps import API


app_name = API.name

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'programmes', views.ProgrammeViewSet)
router.register(r'slots', views.SlotViewSet)
router.register(r'episodes', views.EpisodeViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(
    r'transmissions', views.TransmissionViewSet, basename='transmission')

urlpatterns = router.urls
