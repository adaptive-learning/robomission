import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from learn.export import ActionSerializer
from learn.models import Action


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Action, dispatch_uid='learn.signals.log_new_action')
def log_new_action(sender, instance, created, **kwargs):
    action = instance
    if created:
        logger.info('Action %s', ActionSerializer(action).data)
