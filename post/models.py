from django.db import models
from models_utils.models import BaseModel
from account.models import Profile


class Post(BaseModel):
    content = models.CharField(max_length=250)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Post {self.content} by {self.author.user}'
