from django.dispatch import receiver
from django.db.models.signals import post_save
from core.models import User
from core.tasks import account_created_task

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_registration_mail(sender, instance, created, **kwargs):
    if created:
        account_created_task.delay(instance.id)
        return True
    return False
