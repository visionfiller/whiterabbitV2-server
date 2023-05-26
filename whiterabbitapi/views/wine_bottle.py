from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import WineBottle


class WineBottleView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            wine_bottle = WineBottle.objects.get(pk=pk)
            serializer = WineBottleSerializer(wine_bottle)
            return Response(serializer.data)
        except WineBottle.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        wine_bottles = WineBottle.objects.all()
        varietal_region_id = request.query_params.get('varietal_region', None)
        if varietal_region_id is not None:
            wine_bottles = wine_bottles.filter(varietal_region__id=varietal_region_id)
        serializer = WineBottleSerializer(wine_bottles, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
             Response -- JSON serialized game instance
        """
        serializer = CreateWineBottleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
           
           
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        """delete varietal region"""
        wine_bottle= WineBottle.objects.get(pk=pk)
        wine_bottle.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
class CreateWineBottleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineBottle
        fields = ['id', 'name','vintage', 'varietal_region', 'image', 'link']
class WineBottleSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = WineBottle
        fields = ('id', 'name','vintage', 'varietal_region', 'image', 'link')
        depth =1