from django.db import models
from account.models import User


# Create your models here.
class Follow(models.Model):
    followed_by = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="followed_by"
    )
    followed_to = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="followed_to"
    )
    created_at = models.DateTimeField(auto_now_add=True)
