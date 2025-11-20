from rest_framework import serializers
from .models import Tweet, Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'username', 'tweet', 'text', 'created_at']
        # We make 'tweet' read-only so we don't have to send it when just reading
        extra_kwargs = {'tweet': {'required': False}}

class TweetSerializer(serializers.ModelSerializer):
    # ReadOnlyField: We want to display the username, 
    # but we don't want the user to be able to edit it.
    username = serializers.ReadOnlyField(source='user.username')

    # NESTED SERIALIZER: This puts the actual comment data inside the Tweet JSON
    # read_only=True means we cannot CREATE comments via the Tweet API (we will use a separate endpoint)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'username', 'content', 'image', 'video', 'shares_count', 'comments', 'created_at']
        # 'user' is not here because we will assign it automatically in the View