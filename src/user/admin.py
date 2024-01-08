from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User

    list_display = ['fullname', 'username', 'email', 'created_at']
    list_filter = ['username']
    search_fields = ['fullname']

admin.site.register(User, UserAdmin)
