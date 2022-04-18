from django.db import models

from applicase.models import TAPositionPost, User
from django.utils import timezone
from django.contrib.auth import get_user_model

class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    position = models.ForeignKey(TAPositionPost, on_delete=models.CASCADE)
    context = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        template = 'Author: {0.author}, Application: [{0.application}]'
        return template.format(self)