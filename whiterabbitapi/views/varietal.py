"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Varietal


class VarietalView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            varietal = Varietal.objects.get(pk=pk)
            serializer = VarietalSerializer(varietal)
            return Response(serializer.data)
        except Varietal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        varietals = Varietal.objects.all()
        serializer = VarietalSerializer(varietals, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
             Response -- JSON serialized game instance
        """
        serializer = CreateVarietalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
           
           
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        """delete varietal region"""
        varietal= Varietal.objects.get(pk=pk)
        varietal.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
class CreateVarietalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varietal
        fields = ['id', 'name', 'image', 'description', 'wine_type']
class VarietalSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Varietal
        fields = ('id', 'name', 'image', 'description', 'wine_type')
        depth =1