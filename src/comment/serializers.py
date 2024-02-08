from .models import Comment, ReplyToComment
from rest_framework import serializers


class ReplyToCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToComment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    def getReplies(self, obj):
        replies = ReplyToComment.objects.filter(comment=obj.id).all()
        serializers = ReplyToCommentSerializer(replies, many=True)
        return serializers.data

    replies = serializers.SerializerMethodField("getReplies")

    class Meta:
        model = Comment
        fields = "__all__"
