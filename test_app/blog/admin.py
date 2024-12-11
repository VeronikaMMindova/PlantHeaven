from django.contrib import admin

from test_app.blog.models import Post, Category, Plant, Comment
from test_app.users.models import Profile


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'category', 'description', 'snippet', 'image', 'is_deleted']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    fields = ['name', 'habitat', 'type_of_plant', 'category', 'image', 'wikipedia_url']

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    pass