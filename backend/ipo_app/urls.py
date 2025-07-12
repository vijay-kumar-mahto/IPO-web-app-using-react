from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_root import api_root

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'ipos', views.IPOViewSet, basename='ipo')
router.register(r'documents', views.DocumentViewSet, basename='document')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', api_root, name='api-root'),  # Custom API root view
    path('', include(router.urls)),
]