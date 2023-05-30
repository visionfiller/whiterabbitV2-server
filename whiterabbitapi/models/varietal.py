from django.db import models


class Varietal(models.Model):
    name = models.CharField(max_length=155)
    image = models.CharField(max_length=155)
    description = models.CharField(max_length=500)
    wine_type =models.ForeignKey("WineType",on_delete=models.CASCADE)