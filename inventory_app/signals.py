from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InventoryItem, InventoryChange

@receiver(post_save, sender=InventoryItem)
def log_inventory_change(sender, instance, created, **kwargs):
    if not created:
        try:
            old_instance = InventoryItem.objects.get(pk=instance.pk)
            if old_instance.quantity != instance.quantity:
                quantity_change = instance.quantity - old_instance.quantity
                InventoryChange.objects.create(
                    item=instance,
                    quantity_change=quantity_change,
                    user=instance.owner
                )
        except InventoryItem.DoesNotExist:
            pass