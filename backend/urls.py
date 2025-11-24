from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token # <--- IMPORT THIS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tweets.urls')),
    
    # ADD THIS LINE for Login to work:
    path('api-token-auth/', obtain_auth_token), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)