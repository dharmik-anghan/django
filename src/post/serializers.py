from rest_framework import serializers
from comment.models import Comment
from comment.serializers import CommentSerializer
from follow.models import Follow
from like.models import Like
from post.models import Post, PostImage
import random
POST_STATUS_CHOICES = (
    ("published", "published"),
    ("private", "private"),
)


class PostImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostImage
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.image.url
        return request.build_absolute_uri(image)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageCreateSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Post
        fields = ["id", "images", "description", "user_id", "status", "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        post = Post.objects.create(**validated_data)

        for image in uploaded_images:
            PostImage.objects.create(post=post, image=image)
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "description", "user_id", "status"]


class GetFeedSerializer(serializers.ModelSerializer):
    def getPost(self, obj):
        posts = Post.objects.filter(user_id=obj.followed_to.id).all()
        images = []
        serializers = PostSerializer(posts, many=True)
        for post in posts:
            if post.status == "draft" or post.status=="private":
                continue
            data = {}
            serializers = PostSerializer(post)

            img = PostImage.objects.filter(post=post).all()
            image_serializer = PostImageSerializer(
                img, context=self.context, many=True
            )
            data.update(serializers.data)
            data.update({"following": Follow.objects.filter(followed_by=obj.followed_by.id, followed_to=post.user_id.id).exists()})
            data.update({"liked": Like.objects.filter(user=obj.followed_by.id, post=post, comment=None, reply=None).exists()})
            data.update({"images": image_serializer.data})
            comments = Comment.objects.filter(post=post).all()
            comment_serializer = CommentSerializer(comments, many=True)
            data.update({"comments" : comment_serializer.data})
            images.append(data)
        return images

    posts = serializers.SerializerMethodField("getPost")

    class Meta:
        model = Follow
        fields = ("posts",)
        read_only_fields = ("id",)
