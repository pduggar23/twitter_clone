from rest_framework import viewsets, permissions,status
from rest_framework.parsers import MultiPartParser, FormParser
from tweets.tasks import moderate_content, notify_followers, resize_image
from .models import Tweet,Comment
from .serializers import CommentSerializer, TweetSerializer
from rest_framework.decorators import action

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at') # Newest tweets first
    serializer_class = TweetSerializer
    
    # 1. Security: Users must be logged in to post, but anyone can read
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 2. The Magic: This tells Django "Expect files, not just JSON"
    parser_classes = (MultiPartParser, FormParser)

    # 3. Automation: Auto-assign the 'user' field when saving
    def perform_create(self, serializer):
        # 1. Save the raw tweet
        tweet = serializer.save(user=self.request.user)
        
        # 2. Trigger the Background Pipeline
        # We pass the ID, not the whole object, because passing objects to Celery is risky
        
        # A. Notify Followers
        notify_followers.delay(tweet.user.username, tweet.content)
        
        # B. Check for bad words
        moderate_content.delay(tweet.id)
        
        # C. Resize Image (if one exists)
        if tweet.image:
            resize_image.delay(tweet.id)
            
    # This creates a new URL: POST /api/tweets/{id}/share/
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        tweet = self.get_object() # Get the tweet by ID (pk)
        tweet.shares_count += 1   # Increment count
        tweet.save()              # Save to DB
        return Response({'status': 'shared', 'shares_count': tweet.shares_count})
    
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)