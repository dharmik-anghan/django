from django.db import models

# Create your models here.
class Comment(models.Model):
    comment = models.CharField(max_length=300)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(null=True)
    reply_count  = models.IntegerField(null=True)
    
class ReplyToComment(models.Model):
    reply = models.CharField(max_length=300)
    comment = models.ForeignKey("comment.Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(null=True)
