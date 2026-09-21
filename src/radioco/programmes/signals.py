from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from radioco.programmes.models import Programme


@receiver(pre_save, sender=Programme)
def generate_slug(instance, **kwargs):
    instance.slug = slugify(instance.name)
