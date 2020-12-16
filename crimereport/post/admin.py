from django.contrib import admin
from .models import Post, Comment
# Register your models here.
@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','author','title','photo','text','created','updated']
    readonly_fields = ('created', 'updated')

@admin.register(Comment)
class UserAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'text', 'created', 'updated']
