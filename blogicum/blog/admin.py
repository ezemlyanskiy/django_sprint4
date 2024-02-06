from django.contrib import admin

from .models import Category, Comment, Location, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)
    list_display = (
        'title',
        'text',
        'author',
        'location',
        'category',
        'created_at',
        'is_published',
    )
    list_editable = ('is_published',)
    list_filter = (
        'category',
        'created_at',
        'is_published',
    )
    search_fields = ('title',)
    empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'title',
        'description',
        'slug',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
        'slug',
    )
    list_filter = (
        'created_at',
        'is_published',
    )
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'name',
        'created_at',
        'is_published',
    )
    list_editable = ('is_published',)
    list_filter = (
        'created_at',
        'is_published',
    )
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = ('text',)
