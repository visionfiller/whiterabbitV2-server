from django.db import models


class VarietalRegion(models.Model):
    varietal =models.ForeignKey("Varietal",on_delete=models.CASCADE)
    region = models.ForeignKey("Region",on_delete=models.CASCADE, related_name="varietal_regions")
    body =  models.ForeignKey("Body",on_delete=models.CASCADE)
    dryness =  models.ForeignKey("Dryness",on_delete=models.CASCADE)
    acidity =  models.ForeignKey("Acidity",on_delete=models.CASCADE)

    @property
    def is_favorite(self):
        return self.__is_favorite
    # TODO: Add a `is_favorite` custom property. Remember each JSON representation of a restaurant should have a `is_favorite` property. Not just the ones where the value is `true`.
    @is_favorite.setter
    def is_favorite(self, value):
        self.__is_favorite = value
    
    