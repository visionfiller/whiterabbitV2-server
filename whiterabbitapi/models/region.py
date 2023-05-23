from django.db import models


class Region(models.Model):
    location = models.CharField(max_length=155)
    geo_code_city = models.CharField(max_length=155)
    country = models.CharField(max_length=155)
    