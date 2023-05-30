from django.db import models


class Varietal(models.Model):
    name = models.CharField(max_length=155)
    image = models.CharField(max_length=155)
    description = models.TextField()
    wine_type =models.ForeignKey("WineType",on_delete=models.CASCADE)