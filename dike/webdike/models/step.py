from django.db import models
import django.contrib.postgres.fields as pgfields


from .sentence import Sentence


class Step(models.Model):
    SPLITTED = 0
    POLISHED = 1
    CONNECTED = 2
    EXPLAINED = 3
    STAGE_CHOICES = (
        (SPLITTED, 'Splitted'),
        (POLISHED, 'Polished'),
        (CONNECTED, 'Connected'),
        (EXPLAINED, 'Explained'),
    )

    stage = models.IntegerField(
        choices=STAGE_CHOICES,
    )
    sentence = models.ForeignKey(Sentence)
    vote = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    result = pgfields.JSONField()
    parent_step = models.ForeignKey('self', blank=True)
