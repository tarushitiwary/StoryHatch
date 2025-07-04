from django.contrib import admin
from .models import Story, Chapter, Comment, Bookmark

admin.site.register(Story)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(Bookmark)

from django.contrib import admin
from .models import Profile, Story, Chapter

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_public', 'created_at']
    list_filter = ['is_public']
    search_fields = ['title', 'summary', 'author__username']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['story', 'chapter_number', 'created_by', 'parent_chapter']
    search_fields = ['story__title']
