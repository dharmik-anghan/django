from django.contrib import admin
from .models import Post, PostImage


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_id",
        "description",
        "status",
        "created_at",
        "updated_at",
        "like_count",
        "comment_count",
    ]
    list_editable = ["status"]


class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "image",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
