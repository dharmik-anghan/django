from rest_framework.views import APIView
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from post.serializers import PostSerializer,PostCreateSerializer, PostUpdateSerializer
from post.models import Post
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from datetime import datetime, timezone
# Create your views here.


class GetPostView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        post_id = request.query_params.get("id")

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({"msg": "Post not found"}, status=404)


            serializer = PostSerializer(post, context={'request':request})
            return Response({"post": serializer.data})
        
    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id

        serializer = PostCreateSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        

    def patch(self, request):
        data = request.data
        post_id = request.query_params.get('id')
        post = Post.objects.get(pk=post_id)
        post.updated_at = datetime.now(timezone.utc)
        post.save()
        serializer = PostUpdateSerializer(post, data=data, partial=True, context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    def delete(self, request):
        post_id = request.query_params.get('id')
        post = Post.objects.get(pk=post_id)
        post.delete()
        return Response({"msg": "Post Deleted"}, status=204)

class GetImageFile(APIView):
    def get(self, request, username, filename):
        html = """
            <img src="/media/uploads/admin/1706184713.jpg">
"""


