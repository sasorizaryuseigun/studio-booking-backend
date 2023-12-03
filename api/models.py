from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import uuid as uuid_lib

User = get_user_model()


class TimeTableTemplate(models.Model):
    DAYS = (
        (1, _("月曜日")),
        (2, _("火曜日")),
        (3, _("水曜日")),
        (4, _("木曜日")),
        (5, _("金曜日")),
        (6, _("土曜日")),
        (7, _("日曜日")),
    )

    day = models.PositiveSmallIntegerField(
        verbose_name=_("曜日"),
        editable=False,
        choices=DAYS,
        validators=(validators.MinLengthValidator(1), validators.MaxLengthValidator(7)),
    )
    time = models.TimeField(verbose_name=_("開始時刻"), editable=False)
    price = models.PositiveIntegerField(verbose_name=_("価格"), blank=True, null=True)
    enable = models.BooleanField(verbose_name=_("有効"), default=False)

    class Meta:
        ordering = ["day", "time"]
        constraints = (
            models.UniqueConstraint(fields=("day", "time"), name="day_and_time"),
        )


class TimeTable(models.Model):
    time = models.DateTimeField(verbose_name=_("開始日時"), editable=False, unique=True)
    price = models.PositiveIntegerField(verbose_name=_("価格"), blank=True, null=True)
    enable = models.BooleanField(verbose_name=_("有効"), default=False)

    def __str__(self):
        return str(self.time)

    @property
    def booking(self):
        model = Booking

        try:
            model.objects.get(enable=True, end__gt=self.time, start__lte=self.time)

        except model.DoesNotExist:
            return False

        except model.MultipleObjectsReturned:
            return True

        else:
            return True

    class Meta:
        ordering = ["time"]


class Booking(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"), unique=True, default=uuid_lib.uuid4, editable=False
    )
    user = models.ForeignKey(
        User, verbose_name=_("予約者"), on_delete=models.SET_NULL, null=True
    )
    start = models.DateTimeField(verbose_name=_("開始時刻"))
    end = models.DateTimeField(verbose_name=_("終了時刻"))
    booking = models.DateTimeField(verbose_name=_("予約時刻"), auto_now_add=True)
    enable = models.BooleanField(verbose_name=_("有効"), default=True)
    canceled = models.DateTimeField(verbose_name=_("取消時刻"), blank=True, null=True)

    def delete(self):
        if self.enable:
            self.enable = False
            self.save()

    class Meta:
        ordering = ["start", "end"]
