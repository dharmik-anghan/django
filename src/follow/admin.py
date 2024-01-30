from django.contrib import admin
from .models import Follow
# Register your models here.
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'followed_by', 'followed_to']

admin.site.register(Follow, FollowAdmin)