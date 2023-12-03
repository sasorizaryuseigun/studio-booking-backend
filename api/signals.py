from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Booking, TimeTableTemplate, TimeTable


@receiver(pre_save, sender=Booking)
def receiverBooking(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.enable and not (instance.enable):
            instance.canceled = timezone.now()

    except sender.DoesNotExist:
        if not (instance.enable):
            instance.canceled = timezone.now()


@receiver(pre_save, sender=TimeTableTemplate)
def receiverTimeTableTemplate(sender, instance, **kwargs):
    if instance.price is None:
        instance.enable = False


@receiver(pre_save, sender=TimeTable)
def receiverTimeTable(sender, instance, **kwargs):
    if instance.price is None:
        instance.enable = False
