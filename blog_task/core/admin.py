from django.contrib import admin
from .models import Blog, Category, Comment, AboutPageModel, Contact, ContactPageData


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    readonly_fields = ('slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'ordering',)
    readonly_fields = ('slug',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'blog')


@admin.register(AboutPageModel)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')


@admin.register(ContactPageData)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
