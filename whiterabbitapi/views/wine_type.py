"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import WineType


class WineTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            wine_type = WineType.objects.get(pk=pk)
            serializer = WineTypeSerializer(wine_type)
            return Response(serializer.data)
        except WineType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        wine_types = WineType.objects.all()
        serializer = WineTypeSerializer(wine_types, many=True)
        return Response(serializer.data)
   
    def destroy(self, request, pk):
        """delete WineType region"""
        wine_type= WineType.objects.get(pk=pk)
        wine_type.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
class CreateWineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineType
        fields = ['id', 'type']
class WineTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = WineType
        fields = ('id', 'type')
        