from django.db import models


class WineType(models.Model):
    type = models.CharField(max_length=155)
    