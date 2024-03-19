from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from radioco.schedules.models import Schedule
from radioco.schedules import utils


@receiver(post_save, sender=Schedule)
@receiver(post_delete, sender=Schedule)
def rearrange_episodes(instance, **kwargs):
    utils.rearrange_episodes(instance.slot.programme, timezone.now())
