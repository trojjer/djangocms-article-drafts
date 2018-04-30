from django.dispatch import receiver
from django.db.models.signals import post_save

from .mixins import GenericPublishMixin


@receiver(post_save, dispatch_uid='generic_publish_event')
def publish_event(sender, instance, **kwargs):
    # check the settings PUBLISHER_REGISTERED_MODELS for known publishable models

    # get the model
    # e.g. model.save()
    pass
