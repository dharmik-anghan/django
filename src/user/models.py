from django.db import models

# Create your models here.
class User(models.Model):
    fullname = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=30, null=False, unique=True, blank=False)
    email = models.EmailField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None)
    password = models.CharField(null=False)
    last_login = models.DateTimeField(null=True, default=None)

    def __str__(self) -> str:
        return str(self.id) + ' | ' + str(self.username)