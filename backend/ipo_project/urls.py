"""
URL configuration for ipo_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root URL to API root
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('ipo_app.urls')),
    path('api/home/', include('home.urls')),
    path('api/broker/', include('broker.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)