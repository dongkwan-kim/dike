from django.db import models
import django.contrib.postgres.fields as pgfields


class Step(models.Model):
    SPLITTED = 'SP'
    POLISHED = 'PO'
    CONNECTED = 'CN'
    EXPLAINED = 'EX'
    STAGE_CHOICES = (
        (SPLITTED, 'Splitted'),
        (POLISHED, 'Polished'),
        (CONNECTED, 'Connected'),
        (EXPLAINED, 'Explained'),
    )

    stage = models.CharField(
        max_length=2,
        choices=STAGE_CHOICES,
    )
    sid = models.IntegerField()
    vote = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    result = pgfields.JSONField()


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

