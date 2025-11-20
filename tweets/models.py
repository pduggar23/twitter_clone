from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    # 1. Who posted this?
    # on_delete=models.CASCADE: If user is deleted, delete their tweets too.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    
    # 2. The Text Content
    # blank=True means they can post JUST an image without text if they want.
    content = models.TextField(blank=True)
    
    # 3. Media Files
    # upload_to tells Django which folder INSIDE 'media' to put these files.
    image = models.ImageField(upload_to='tweet_images/', blank=True, null=True)
    video = models.FileField(upload_to='tweet_videos/', blank=True, null=True)
    
    # 4. Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 5. Interactions
    # We keep it simple: just a number. 
    # (In a massive app, this would be a separate table, but this is fine for now).
    shares_count = models.IntegerField(default=0)
    
    def __str__(self):
        # Show the first 20 chars of the tweet in Admin
        return f"{self.user.username}: {self.content[:20]}..."
    
class Comment(models.Model):
    # Link to the User who commented
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Link to the Tweet (related_name='comments' lets us grab tweet.comments later)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on Tweet {self.tweet.id}"