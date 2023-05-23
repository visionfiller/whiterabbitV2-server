from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=150)
    favorites = models.ManyToManyField("VarietalRegion", through="Favorite", related_name="customers")
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'