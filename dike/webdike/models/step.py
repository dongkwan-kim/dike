from django.db import models
import django.contrib.postgres.fields as pgfields
import json

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
    result = pgfields.ArrayField(models.TextField(), default=[])
    parent_step = models.ForeignKey('self', null=True)

    def to_json(self):
        """Return id and result in json format. Used in template"""
        return json.dumps({
            'id': self.id, 'result': self.result, 'parent_id': self.parent_step_id })
