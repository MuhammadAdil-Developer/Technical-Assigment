from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

# Create a router for the viewset


router= DefaultRouter()
router.register("auth", UserAuthViewset, basename="auth")
router.register("projects", ProjectViewSet, basename="projects")


urlpatterns = [
    
]

urlpatterns += router.urls
