from django.urls import path
from post.views import GetPostView

urlpatterns = [
    path("", GetPostView.as_view()),
]

