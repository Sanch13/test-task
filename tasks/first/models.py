from django.db import models


class RatesDay(models.Model):
    date = models.DateField(unique=True)
    data = models.JSONField()


