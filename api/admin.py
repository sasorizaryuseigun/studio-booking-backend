from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest

from .models import Booking, TimeTable, TimeTableTemplate


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "enable")
    readonly_fields = ("booking", "canceled")
    list_filter = ("enable",)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TimeTableTemplate)
class TimeTableTemplateAdmin(admin.ModelAdmin):
    list_display = ("day", "time", "price", "enable")
    list_display_links = None
    list_editable = ("price", "enable")
    readonly_fields = ("day", "time")
    list_filter = ("enable",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ("time", "price", "enable", "booking")
    list_display_links = None
    list_editable = ("price", "enable")
    readonly_fields = ("time",)
    list_filter = ("enable",)
    date_hierarchy = "time"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
