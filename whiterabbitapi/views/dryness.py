"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Dryness


class DrynessView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            dryness = Dryness.objects.get(pk=pk)
            serializer = DrynessSerializer(dryness)
            return Response(serializer.data)
        except Dryness.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        drynesses = Dryness.objects.all()
        serializer = DrynessSerializer(drynesses, many=True)
        return Response(serializer.data)

class DrynessSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Dryness
        fields = ('id', 'level','tastes_like')
        