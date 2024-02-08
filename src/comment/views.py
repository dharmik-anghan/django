from .models import Comment, ReplyToComment
from post.models import Post
from rest_framework.response import Response
from rest_framework.views import APIView
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer, ReplyToCommentSerializer


class CommentView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def update_comment_reply_count(self, post_id):
        total_comment_count = (
            ReplyToComment.objects.filter(post=post_id).count()
            + Comment.objects.filter(post=post_id).count()
        )
        post = Post.objects.get(pk=post_id)
        post.comment_count = total_comment_count
        post.save()

    def get(self, request):
        data = request.data
        data["user"] = request.user.id
        try:
            comments = Comment.objects.get(pk=data["comment"], post=data["post"])
        except Comment.DoesNotExist:
            return Response({"msg": "Comment Doesn't Exists"}, status=404)

        serializer = CommentSerializer(comments)
        return Response({"msg": serializer.data}, status=200)

    def post(self, request, *args, **kwargs):
        if not Post.objects.filter(pk=request.data.get("post")).exists():
            return Response({"msg": "Post not found"}, status=404)

        data = request.data
        data["user"] = request.user.id
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.update_comment_reply_count(request.data.get("post"))

        return Response({"comment": serializer.data}, status=201)

    def delete(self, request, *args, **kwargs):
        comment_id = request.data.get("comment")
        user_id = request.user.id
        if Comment.objects.filter(pk=comment_id).exists():
            comment = Comment.objects.get(pk=comment_id)
            if user_id == comment.user.id or user_id == comment.post.user_id.id:
                comment.delete()
                self.update_comment_reply_count(request.data.get("post"))
                return Response({"msg": "Comment Deleted"}, status=204)
            else:
                return Response({"msg": "Comment not found"}, status=404)
        else:
            return Response({"msg": "Can't perform this action"}, status=400)


class ReplyToCommentView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = ReplyToCommentSerializer

    def update_reply_count(self, comment_id, post_id):
        comment = Comment.objects.get(pk=comment_id)
        reply_count = ReplyToComment.objects.filter(comment=comment_id).count()
        comment.reply_count = reply_count
        comment.save()

        total_comment_count = (
            ReplyToComment.objects.filter(post=post_id).count()
            + Comment.objects.filter(post=post_id).count()
        )
        post = Post.objects.get(pk=post_id)
        post.comment_count = total_comment_count
        post.save()

    def post(self, request, *args, **kwargs):
        if not Comment.objects.filter(pk=request.data.get("comment")).exists():
            return Response({"msg": "Comment not found"}, status=404)

        data = request.data
        data["user"] = request.user.id
        serializer = ReplyToCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.update_reply_count(data["comment"], data['post'])

        return Response({"reply": serializer.data}, status=201)

    def delete(self, request, *args, **kwargs):
        reply_id = request.data.get("reply")
        post_id = request.data.get("post")
        user_id = request.user.id
        comment_id = request.data.get("comment")
        if ReplyToComment.objects.filter(pk=reply_id).exists():
            reply = ReplyToComment.objects.get(pk=reply_id)
            if user_id == reply.user.id or user_id == reply.post.user_id.id:
                reply.delete()
                self.update_reply_count(comment_id, post_id)
                return Response({"msg": "Reply Deleted"}, status=204)
            else:
                return Response({"msg": "Can't delete"}, status=400)
        else:
            return Response({"msg": "Reply not found"}, status=404)
