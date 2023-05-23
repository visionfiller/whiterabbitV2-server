
from django.db import models


class Favorite(models.Model):
    """Favorite Restaurant model
        
    """
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="favoritedWine")
    varietal_region = models.ForeignKey(
        "VarietalRegion", on_delete=models.CASCADE, related_name="winos")
