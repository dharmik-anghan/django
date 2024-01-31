from rest_framework.views import APIView
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from follow.models import Follow
from post.serializers import GetFeedSerializer, PostSerializer, PostCreateSerializer, PostUpdateSerializer
from post.models import Post
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from datetime import datetime, timezone
from account.models import User

# Create your views here.


class GetPostView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def update_post_count(self, user_id):
        post_count = Post.objects.filter(user_id=user_id).count()
        user = User.objects.get(id=user_id)
        user.post_count = post_count
        user.save()

    def get(self, request):
        post_id = request.query_params.get("id")

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({"msg": "Post not found"}, status=404)

            serializer = PostSerializer(post, context={"request": request})
            return Response({"post": serializer.data})

    def post(self, request):
        data = request.data
        data["user_id"] = request.user.id

        serializer = PostCreateSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            self.update_post_count(request.user.id)
            return Response(serializer.data, status=201)
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
            post, data=data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

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
        print(users)
        serializer = GetFeedSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)
