import strawberry
from strawberry import auto
from typing import List, Optional
from . import models

@strawberry.django.type(models.User)
class UserType:
    username: auto
    email: auto

@strawberry.django.type(models.Comment)
class CommentType:
    id: auto
    text: auto
    user: UserType # Nested relationship!
    created_at: auto

@strawberry.django.type(models.Tweet)
class TweetType:
    id: auto
    content: auto
    username: str # Custom field logic
    created_at: auto
    shares_count: auto
    # We can fetch comments for a tweet directly
    comments: List[CommentType]

    # Custom resolver for username (like SerializerMethodField)
    @strawberry.field
    def username(self) -> str:
        return self.user.username