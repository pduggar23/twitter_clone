import strawberry
from typing import List
from .models import Tweet
from .types import TweetType

@strawberry.type
class Query:
    # 1. Get All Tweets
    @strawberry.field
    def tweets(self) -> List[TweetType]:
        # We use select_related just like in REST to optimize DB queries
        return Tweet.objects.select_related('user').prefetch_related('comments__user').order_by('-created_at')

    # 2. Get Single Tweet
    @strawberry.field
    def tweet(self, id: int) -> TweetType:
        return Tweet.objects.get(id=id)

schema = strawberry.Schema(query=Query)