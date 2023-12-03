from rest_framework import routers
from .views import BookingAPIView, TimeTableAPIView

router = routers.DefaultRouter()
router.register("booking", BookingAPIView)
router.register("timetable", TimeTableAPIView)
