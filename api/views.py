from rest_framework import viewsets, mixins, permissions, status
from .models import Booking, TimeTable
from .serializers import BookingSerializer, TimeTableSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class BookingAPIView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    class Mata:
        lookup_field = "uuid"

    def get_queryset(self):
        return Booking.objects.filter(
            user=User.objects.get(email="admin@example.com"), enable=True
        )

    def perform_create(self, serializer):
        serializer.save(user=User.objects.get(email="admin@example.com"))


class TimeTableAPIView(viewsets.GenericViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, url_path=r"(?P<date>\d{4}-\d{2}-\d{2})")
    def list_by_date(self, request, date=None):
        try:
            d_date = datetime.date(*[int(i) for i in date.split("-")])
        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        time = datetime.time(hour=0, minute=0)
        s_date = datetime.datetime.combine(d_date, time)
        e_date = datetime.datetime.combine(d_date + datetime.timedelta(days=1), time)

        queryset = self.queryset.filter(time__gte=s_date, time__lt=e_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
