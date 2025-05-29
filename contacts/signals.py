from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Contact
from starfish.utils import get_the_totals

@receiver(post_save, sender=Contact)
def contact_post_save(sender, instance, created, **kwargs):
    total = get_the_totals()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'totals_group',
        {
            'type': 'totals.update',
            'message': json.dumps({'total': total}),
        }
    )
