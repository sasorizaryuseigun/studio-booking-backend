from django.apps import AppConfig

import datetime


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from . import signals

    #     from .models import TimeTableTemplate, TimeTable

    #     for i in range(7):
    #         for ii in range(24):
    #             for iii in range(0, 60, 15):
    #                 time = datetime.time(hour=ii, minute=iii)
    #                 TimeTableTemplate.objects.get_or_create(day=i+1, time=time)

    #     today = datetime.date.today()
    #     for i in range(31):
    #         day = today + datetime.timedelta(days=i)
    #         for ii in range(24):
    #             for iii in range(0, 60, 15):
    #                 time = datetime.time(hour=ii, minute=iii)
    #                 date = datetime.datetime.combine(day, time)
    #                 temp = TimeTableTemplate.objects.get(day=day.weekday() + 1, time=time)
    #                 TimeTable.objects.get_or_create(time=date, defaults={"price": temp.price, "enable": temp.enable})
