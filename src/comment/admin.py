from django.contrib import admin
from .models import Comment, ReplyToComment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'user', 'post', 'created_at', 'like_count', 'reply_count']

class ReplyToCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'reply', 'comment','user', 'post', 'created_at', 'like_count']

admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyToComment, ReplyToCommentAdmin)
