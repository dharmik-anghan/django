from django.urls import path
from .views import FollowViews, GetFollowerView, GetFollowingView

urlpatterns = [
    path("", FollowViews.as_view()),
    path("followers", GetFollowerView.as_view()),
    path("following", GetFollowingView.as_view()),
]
