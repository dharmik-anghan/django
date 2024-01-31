from django.urls import path
from post.views import GetPostView, GetPostFeedView

urlpatterns = [
    path("", GetPostView.as_view()),
    path("feed", GetPostFeedView.as_view()),
]

