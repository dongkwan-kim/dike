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
    POPULATION_DEFAULT = 2

    stage = models.IntegerField(
        choices=STAGE_CHOICES,
    )
    sentence = models.ForeignKey(Sentence)
    vote = models.IntegerField(default=1)
    population = models.FloatField(default=POPULATION_DEFAULT)
    result = pgfields.ArrayField(models.TextField(), default=[])
    parent_step = models.ForeignKey('self', null=True)

    def __str__(self):
        return 'Step --id-{} --stage-{} --vote-{} --pop-{}'\
            .format(str(self.id), str(self.stage), str(self.vote), str(self.population))

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

        :param K: total carrying capacity
        :return: float
        """
        N = self.population
        if N == 0:
            return 0

        # Get maximum growth rate, r(v),
        rv = self.get_max_growth_rate()

        # Get carrying capacity, k(v, K),
        k = self.get_carrying_capacity(K)

        # Return r(v) * N * (1 - N/K)
        r = rv * N * (1 - N/k)
        return r

    def get_max_growth_rate(self):
        """Get maximum growth rate.

        :return: float
        """

        # Get voting counts of Step, v
        v = self.vote

        # Get total voting counts of that generation, tv
        tv = self.get_total_votes()

        return self.POPULATION_DEFAULT * min(tv/10, 1)

    def get_carrying_capacity(self, K):
        """Get carrying capacity.

        :param K: total carrying capacity
        :return: float
        """

        # Get voting counts of Step, v
        v = self.vote

        # Get total voting counts of that generation, tv
        tv = self.get_total_votes()

        if K is 0 or tv is 0:
            print('000')

        # Return K * v/tv
        return K * v/tv

    def stage_name_korean(self):
        if self.stage == self.IMPORTED:
            return '원문'
        elif self.stage == self.SPLITTED:
            return '나누기'
        elif self.stage == self.POLISHED:
            return '다듬기'
        elif self.stage == self.CONNECTED:
            return '잇기'
        else:
            return '설명하기'

    def get_total_votes(self):
        tv = sum([s.vote for s in Step.objects.filter(stage=self.stage, sentence__id=self.sentence.id)])
        return tv
