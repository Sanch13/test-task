from django.db import models


class RateDay(models.Model):
    date = models.DateField()
    cur_id = models.PositiveIntegerField()
    data = models.JSONField()
