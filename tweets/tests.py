import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Tweet

# This mark tells Pytest: "Allow this test to touch the database"
@pytest.mark.django_db
def test_create_tweet():
    # 1. Setup: Create a user
    user = User.objects.create_user(username='testbot', password='password123')
    
    # 2. Setup: Log them in (using the API Client)
    client = APIClient()
    client.force_authenticate(user=user)

    # 3. Action: Post a tweet
    payload = {"content": "Hello from GitHub Actions!"}
    response = client.post('/api/tweets/', payload)

    # 4. Verification (The "Test")
    # Check if the server said "201 Created"
    assert response.status_code == 201
    
    # Check if it actually exists in the DB
    assert Tweet.objects.count() == 1
    assert Tweet.objects.get().content == "Hello from GitHub Actions!"