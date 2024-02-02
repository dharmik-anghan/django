from rest_framework import serializers
from follow.models import Follow
from post.models import Post, PostImage

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
            data = {}
            serializers = PostSerializer(post)

            img = PostImage.objects.filter(post=post).all()
            image_serializer = PostImageSerializer(
                img, context=self.context, many=True
            )
            data.update(serializers.data)
            data.update({"images": image_serializer.data})
            images.append(data)
        return images

    posts = serializers.SerializerMethodField("getPost")

    class Meta:
        model = Follow
        fields = ("posts",)
        read_only_fields = ("id",)
