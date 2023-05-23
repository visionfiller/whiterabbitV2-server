from django.db import models


class Dryness(models.Model):
    level = models.CharField(max_length=155)
    tastes_like = models.CharField(max_length=155)
    