from django.urls import path
from .views import portalCrowling, staffUpdate

urlpatterns = [
    path("test/crowling", portalCrowling),
    path("test/staff", staffUpdate),
]
