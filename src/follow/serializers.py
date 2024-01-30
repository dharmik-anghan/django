from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["followed_to", "followed_by"]


class FollowerSerializer(serializers.ModelSerializer):
    def getUsername(self, obj):
        return obj.followed_by.name

    username = serializers.SerializerMethodField("getUsername")

    class Meta:
        model = Follow
        fields = (
            "id",
            "followed_by",
            "username",
        )
        read_only_fields = ("id",)


class FollowingSerializer(serializers.ModelSerializer):
    def getUsername(self, obj):
        return obj.followed_to.name

    username = serializers.SerializerMethodField("getUsername")

    class Meta:
        model = Follow
        fields = (
            "id",
            "followed_to",
            "username",
        )
        read_only_fields = ("id",)
