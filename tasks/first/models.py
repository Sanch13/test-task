from django.db import models


class RateDay(models.Model):
    date = models.DateField(unique=True)
    data = models.JSONField()


