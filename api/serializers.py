from rest_framework import serializers
from .models import Booking, TimeTable

import datetime


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("uuid", "start", "end")

    def validate(self, data):
        model = Booking
        if data["end"] < data["start"]:
            raise serializers.ValidationError()

        try:
            model.objects.get(enable=True, end__gt=data["start"], start__lt=data["end"])

        except model.DoesNotExist:
            return super().validate(data)

        except model.MultipleObjectsReturned:
            raise serializers.ValidationError()

        else:
            raise serializers.ValidationError()


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ("time", "price", "booking")
