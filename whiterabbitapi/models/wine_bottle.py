from django.db import models

class WineBottle(models.Model):
    name = models.CharField(max_length=155)
    vintage = models.IntegerField()
    varietal_region = models.ForeignKey("VarietalRegion",on_delete=models.CASCADE)
    image = models.CharField(max_length=155)
    link = models.CharField(max_length=155)
    