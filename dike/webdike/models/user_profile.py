from django.db import models
from django.contrib.auth.models import User

from .sentence import Sentence


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    work = models.ManyToManyField(
        Sentence,
        through='UserHistory',
        through_fields=('user_profile', 'sentence')
    )

    def __str__(self):
        return self.user.username
