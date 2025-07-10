from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

class Story(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)


    # Optional:
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='forks')
    stars = models.ManyToManyField(User, related_name='starred_stories', blank=True)

    def is_fork(self):
        return self.parent is not None

    def star_count(self):
        return self.stars.count()

class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='chapters')
    content = models.TextField()
    chapter_number = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_chapter = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Chapter {self.chapter_number} of {self.story.title}"
class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.chapter}"
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.story.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
