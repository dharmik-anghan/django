from django.urls import path
from like.views import CommentLikeView

urlpatterns = [
    path("like/", CommentLikeView.as_view(), name="like"),
]