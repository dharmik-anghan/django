from django.urls import path
from comment.views import CommentView, ReplyToCommentView

urlpatterns = [
    path("", CommentView.as_view(), name="comment"),
    path("reply/", ReplyToCommentView.as_view(), name="reply"),
]