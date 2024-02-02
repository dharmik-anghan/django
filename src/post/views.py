from rest_framework.views import APIView
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from follow.models import Follow
from post.serializers import (
    GetFeedSerializer,
    PostSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostImageSerializer,
)
from post.models import Post, PostImage
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from datetime import datetime, timezone
from account.models import User
from django.shortcuts import get_object_or_404

# Create your views here.


class GetPostView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def update_post_count(self, user_id):
        post_count = Post.objects.filter(user_id=user_id).count()
        user = User.objects.get(id=user_id)
        user.post_count = post_count
        user.save()

    @staticmethod
    def append_image_data(serializer, image_serializer):
        data = {}
        data.update(serializer)
        data.update({"images": image_serializer})
        return data

    def get(self, request):
        post_id = request.query_params.get("id")
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)

        images = PostImage.objects.filter(post_id=post_id).all()
        image_serializer = PostImageSerializer(
            images, context={"request": request}, many=True
        )

        data = self.append_image_data(serializer.data, image_serializer.data)

        return Response({"post": data}, status=200)

    def post(self, request):
        data = request.data
        data["user_id"] = request.user.id

        serializer = PostCreateSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            self.update_post_count(request.user.id)
            print(serializer.data.get("id"))

            images = PostImage.objects.filter(post_id=serializer.data['id']).all()
            image_serializer = PostImageSerializer(
                images, context={"request": request}, many=True
            )

            data = self.append_image_data(serializer.data, image_serializer.data)
            return Response(data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def patch(self, request):
        data = request.data
        post_id = request.query_params.get("id")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"msg": "Post not found"}, status=404)
        post.updated_at = datetime.now(timezone.utc)
        post.save()
        serializer = PostUpdateSerializer(
            post, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            images = PostImage.objects.filter(post_id=post_id).all()
            image_serializer = PostImageSerializer(
                images, context={"request": request}, many=True
            )

            data = self.append_image_data(serializer.data, image_serializer.data)       
            return Response(data, status=200)
        else:
            return Response(serializer.errors, status=404)

    def delete(self, request):
        post_id = request.query_params.get("id")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"msg": "Post not found"}, status=404)
        post.delete()
        self.update_post_count(request.user.id)
        return Response({"msg": "Post Deleted"}, status=204)


class GetPostFeedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        user_id = request.user.id
        users = Follow.objects.filter(followed_by=user_id).all()
        # posts=Post.objects.filter(user_id=users).all().order_by('created_at').values()
        serializer = GetFeedSerializer(users, many=True, context={"request": request})
        post_feed = []
        for user in serializer.data:
            for post in user['posts']:
                post_feed.append(post)
        return Response(post_feed)
