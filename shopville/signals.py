from background_task.models import Task
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from rest_api.tasks import process_email_task
from shopville.models import Buyer


@receiver(post_save, sender=Buyer)
def buyer_handler(sender, instance: Buyer, **kwargs):
    process_email_task(instance.id, repeat=Task.DAILY, creator=instance)


@receiver(post_delete, sender=Buyer)
def buyer_delete_handler(sender, instance: Buyer, using,**kwargs):
    buyer_task = Task.objects.filter(creator_object_id=instance.id)
    buyer_task.delete()
