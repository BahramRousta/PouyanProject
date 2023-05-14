from django.db import models
from models_utils.models import BaseModel
from account.models import User


class Post(BaseModel):

    content = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} + {self.content}'
