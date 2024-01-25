from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'user_id', 'description', 'status', 'created_at', 'updated_at']
    list_editable = ['status']

admin.site.register(Post, PostAdmin)
