from django.db import models
from datetime import datetime
POST_STATUS_CHOICES = (
    ("draft", "draft"),
    ("published", "published"),
    ("private", "private"),
)


def upload_image(instance, filename):
    name, ext = filename.rsplit(".")
    filename = str(datetime.now().timestamp()).split('.')[0]+'.'+ext
    upload_path = f"uploads/{instance.user_id.name}/{filename}"
    return upload_path


class Post(models.Model):
    image = models.ImageField(upload_to=upload_image, null=False, blank=False)
    description = models.TextField(null=True)
    user_id = models.ForeignKey("account.User", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, default="published", choices=POST_STATUS_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    liked_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
