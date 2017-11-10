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
