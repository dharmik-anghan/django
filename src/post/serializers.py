from rest_framework import serializers
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
        request = self.context.get('request')
        image = obj.image.url
        print(image)
        return request.build_absolute_uri(image)
    

class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','image', 'description', 'user_id', 'status']
    def get_image(self, obj):
            request = self.context.get('request')
            image = obj.image.url
            print(image)
            return request.build_absolute_uri(image)

class PostUpdateSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ['id','image','description', 'user_id', 'status']

    def get_image(self, obj):
            request = self.context.get('request')
            image = obj.image.url
            print(image)
            return request.build_absolute_uri(image)