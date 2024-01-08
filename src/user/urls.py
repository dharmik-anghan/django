from django.urls import path
from .views import UserAPI

urlpatterns = [
    path("", UserAPI.as_view())
]