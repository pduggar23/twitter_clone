from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Comment

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        # instance is the Comment object
        # We want to notify the OWNER of the tweet
        tweet_owner_id = instance.tweet.user.id
        
        # Don't notify if you commented on your own tweet
        if instance.user.id == tweet_owner_id:
            return

        channel_layer = get_channel_layer()
        group_name = f'notifications_{tweet_owner_id}'
        
        message = f"@{instance.user.username} commented: {instance.text[:20]}..."

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification', # Matches function name in Consumer
                'message': message
            }
        )