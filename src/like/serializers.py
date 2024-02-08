from rest_framework import serializers

from like.models import Like


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["post"]


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["comment"]


class LikeReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["reply"]
