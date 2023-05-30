from django.urls import path
from .views import CustomerFavoriteList, VarietalRegionList

urlpatterns = [
    path('reports/customerfavorites', CustomerFavoriteList.as_view()),
    path('reports/regionvarietals', VarietalRegionList.as_view()),

]