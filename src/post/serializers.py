from rest_framework import serializers
from follow.models import Follow
from post.models import Post

POST_STATUS_CHOICES = (
    ("published", "published"),
    ("private", "private"),
)


class PostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.image.url
        return request.build_absolute_uri(image)
        return image


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "image", "description", "user_id", "status"]


class PostUpdateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "image", "description", "user_id", "status"]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.image.url
        print(image)
        return request.build_absolute_uri(image)
    
class GetFeedSerializer(serializers.ModelSerializer):
    def getPost(self, obj):
        posts = Post.objects.filter(user_id=obj.followed_to.id).all()
        serializers = PostSerializer(posts, many=True,context=self.context)
        return serializers.data
        
    posts = serializers.SerializerMethodField("getPost")

    class Meta:
        model = Follow
        fields = (
            "posts",
        )
        read_only_fields = ("id",)