from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from radioco.schedules import utils
from radioco.schedules.models import Schedule


@receiver(post_save, sender=Schedule)
@receiver(post_delete, sender=Schedule)
def rearrange_episodes(instance, **kwargs):
    utils.rearrange_episodes(instance.slot.programme, timezone.now())
