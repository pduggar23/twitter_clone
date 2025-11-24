from rest_framework import serializers
from .models import Tweet, Comment
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


# Add this class (or ensure UserSerializer is available)
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")]
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'username', 'content', 'image', 'video', 'shares_count', 'comments', 'created_at','is_owner','ai_tags']
        # 'user' is not here because we will assign it automatically in the View

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user == obj.user
        return False