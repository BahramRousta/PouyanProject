from django.db import models
from account.models import Profile
from post.models import Post


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment by {self.author.user.username} on {self.post}'


class Reply(models.Model):
    author = models.ForeignKey(Profile,
                               on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='replies')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply on {self.comment}'
