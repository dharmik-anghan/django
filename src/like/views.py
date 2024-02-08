from .models import Like
from post.models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from comment.models import Comment, ReplyToComment
from rest_framework.permissions import IsAuthenticated
from .serializers import LikeCommentSerializer, LikePostSerializer, LikeReplySerializer


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def update_post_like_count(self, post_id):
        like_count = Like.objects.filter(post=post_id).count()
        post = Post.objects.get(pk=post_id)
        post.like_count = like_count
        post.save()

    def update_comment_like_count(self, comment_id):
        liked_count = Like.objects.filter(comment=comment_id).count()
        comment = Comment.objects.get(pk=comment_id)
        print(comment.user.name)
        comment.like_count = liked_count
        comment.save()

    def update_reply_like_count(self, reply_id):
        liked_count = Like.objects.filter(reply=reply_id).count()
        reply = ReplyToComment.objects.get(pk=reply_id)
        reply.like_count = liked_count
        reply.save()

    def post(self, request, post_id: int):
        comment_id = request.data.get("comment")
        reply_id = request.data.get("reply")

        if not Post.objects.filter(pk=post_id).exists():
            return Response({"msg": "Post not found!!!"}, status=404)

        if comment_id and reply_id == None:
            if not Comment.objects.filter(pk=comment_id).exists():
                return Response({"msg": "Comment not found"}, status=404)
            data = request.data
            if Like.objects.filter(
                user=request.user.id, comment=comment_id, reply=None, post=None
            ).exists():
                return Response({"msg": "Comment Liked"}, status=200)
            serializer = LikeCommentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            self.update_comment_like_count(comment_id)
            return Response({"msg": "Comment Liked"}, status=200)
        elif reply_id and comment_id == None:
            if not ReplyToComment.objects.filter(pk=reply_id).exists():
                return Response({"msg": "Reply not found"}, status=404)
            data = request.data
            if Like.objects.filter(
                user=request.user.id, comment=None, reply=reply_id, post=None
            ).exists():
                return Response({"msg": "Reply Liked"}, status=200)
            serializer = LikeReplySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            self.update_reply_like_count(reply_id)
            return Response({"msg": "Reply Liked"}, status=200)
        elif post_id:
            if Like.objects.filter(
                user=request.user.id, comment=None, reply=None, post=post_id
            ).exists():
                return Response({"msg": "Post Liked"}, status=200)
            data = {"user": request.user, "post": post_id}
            serializer = LikePostSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            self.update_post_like_count(post_id)
            return Response({"msg": "Post Liked"}, status=200)
        else:
            return Response({"msg": "Something went wrong"}, status=400)

    def delete(self, request, post_id: int):
        comment_id = request.data.get("comment")
        reply_id = request.data.get("reply")

        if not Post.objects.filter(pk=post_id).exists():
            return Response({"msg": "Post not found!!!"}, status=404)

        if comment_id and reply_id == None:
            if not Comment.objects.filter(pk=comment_id).exists():
                return Response({"msg": "Comment not found"}, status=404)
            if Like.objects.filter(
                user=request.user.id, comment=comment_id, reply=None, post=None
            ).exists():
                Like.objects.get(
                    user=request.user.id, comment=comment_id, reply=None, post=None
                ).delete()
                self.update_comment_like_count(comment_id)
                return Response({"msg": "Like Removed"}, status=200)
            return Response({"msg": "Liked Removed"}, status=200)
        elif reply_id and comment_id == None:
            if not ReplyToComment.objects.filter(pk=reply_id).exists():
                return Response({"msg": "Reply not found"}, status=404)
            if Like.objects.filter(
                user=request.user.id, comment=None, reply=reply_id, post=None
            ).exists():
                Like.objects.get(
                    user=request.user.id, comment=None, reply=reply_id, post=None
                ).delete()
                self.update_reply_like_count(reply_id)
                return Response({"msg": "Reply Like Removed"}, status=200)

            return Response({"msg": "Reply Like Removed"}, status=200)
        elif post_id:
            if Like.objects.filter(
                user=request.user.id, comment=None, reply=None, post=post_id
            ).exists():
                Like.objects.get(
                    user=request.user.id, comment=None, reply=None, post=post_id
                ).delete()
                self.update_post_like_count(post_id)
                return Response({"msg": "Post Like Removed"}, status=200)
            return Response({"msg": "Post Like Removed"}, status=200)
        else:
            return Response({"msg": "Something went wrong"}, status=400)
