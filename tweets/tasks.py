from celery import shared_task
from PIL import Image
import time
import os

# We import the model INSIDE the task to avoid "Circular Import" errors
# (Because models.py might eventually import tasks.py)

@shared_task
def notify_followers(username, content):
    print(f"🚀 [Background] Sending notifications for {username}...")
    time.sleep(2) # Simulate delay
    print(f"✅ [Background] Notifications sent!")

@shared_task
def moderate_content(tweet_id):
    from .models import Tweet 
    
    # 1. Get the tweet from DB
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        print(f"🧐 [Moderation] Checking Tweet #{tweet_id}...")
    except Tweet.DoesNotExist:
        return

    # 2. Define Bad Words
    BAD_WORDS = ['bad', 'stupid', 'hate', 'spam']
    
    # 3. Check and Replace
    original_text = tweet.content.lower()
    is_dirty = False
    
    for word in BAD_WORDS:
        if word in original_text:
            # Replace the bad word with asterisks (case insensitive replace is harder, doing simple replace here)
            tweet.content = tweet.content.replace(word, '*' * len(word))
            is_dirty = True

    # 4. Save only if we changed something
    if is_dirty:
        tweet.save()
        print(f"⚠️ [Moderation] Censored bad words in Tweet #{tweet_id}")
    else:
        print(f"✅ [Moderation] Tweet #{tweet_id} is clean.")

@shared_task
def resize_image(tweet_id):
    from .models import Tweet
    
    tweet = Tweet.objects.get(id=tweet_id)
    
    # 1. Check if there is an image
    if not tweet.image:
        return "No Image"

    print(f"🎨 [Image] Resizing image for Tweet #{tweet_id}...")

    # 2. Open the image using Pillow (PIL)
    # tweet.image.path gives the full location on the hard drive
    img_path = tweet.image.path
    
    with Image.open(img_path) as img:
        # 3. Resize logic (Max width 800px, keep aspect ratio)
        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            
            # 4. Overwrite the original file
            img.save(img_path)
            print(f"✅ [Image] Resized successfully.")
        else:
            print(f"✅ [Image] Image was already small enough.")