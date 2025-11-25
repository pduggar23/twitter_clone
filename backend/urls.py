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

# Add Debug Toolbar URLs only in Debug mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)