from django.db import models

class Document(models.Model):
    title = models.TextField()
    description = models.TextField()
    announced_at = models.DateField()
    last_valid_step_id = models.IntegerField()

