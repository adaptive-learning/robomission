"""Definitions of signals to be fired when something happens.
"""
import logging
#from django.dispatch import receiver
#from django.db.models.signals import post_save


logger = logging.getLogger(__name__)

# Example of a signal definition (currently not used):

#@receiver(post_save, sender=Action, dispatch_uid='learn.signals.log_new_action')
#def log_new_action(sender, instance, created, **kwargs):
#    action = instance
#    if created:
#        logger.info('Action %s', ActionSerializer(action).data)
