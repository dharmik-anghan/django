from django.db import models

# Create your models here.
class Like(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey("comment.Comment", on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey("comment.ReplyToComment", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    