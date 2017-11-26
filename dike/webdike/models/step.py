from django.db import models
import django.contrib.postgres.fields as pgfields
import json

from .sentence import Sentence


class Step(models.Model):
    IMPORTED = 0
    SPLITTED = 1
    POLISHED = 2
    CONNECTED = 3
    EXPLAINED = 4
    STAGE_CHOICES = (
        (IMPORTED, 'Imported'),
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
    population =models.FloatField(default=1)
    result = pgfields.ArrayField(models.TextField(), default=[])
    parent_step = models.ForeignKey('self', null=True)

    def to_dict(self):
        """Return id and result in json format. Used in template"""
        return {
            'id': self.id,
            'result': self.result,
            'sentence_id': self.sentence_id
        }

    def do_vote(self):
        """Increase vote count 1"""
        self.vote += 1
        self.save()

    def get_growth_rate(self, K):
        """Get growth rate of Step who has given sid.

        The equation is dN/dt = r(v) * N * (1 - N/K).

        :param K: carrying capacity
        :return: float
        """
        # Get maximum growth rate, r(v),

        # Return r(v) * N * (1 - N/K)


    def get_max_growth_rate(self):
        """Get maximum growth rate of given Step.

        :return: float
        """

        # Get voting counts of Step, v

        # Get total voting counts of that generation, tv

        # Return a * v/tv (temporarily a = 2)

