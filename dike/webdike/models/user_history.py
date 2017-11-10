from django.db import models

from .sentence import Sentence
from .user_profile import UserProfile


class UserHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    progress = models.IntegerField()
    sentence = models.ForeignKey(Sentence)
    user_profile = models.ForeignKey(UserProfile)
