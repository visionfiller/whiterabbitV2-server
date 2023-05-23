from django.db import models


class Body(models.Model):
    density = models.CharField(max_length=155)
    