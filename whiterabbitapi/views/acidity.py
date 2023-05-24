"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Acidity


class AcidityView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            acidity = Acidity.objects.get(pk=pk)
            serializer = AciditySerializer(acidity)
            return Response(serializer.data)
        except Acidity.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        acidities = Acidity.objects.all()
        serializer = AciditySerializer(acidities, many=True)
        return Response(serializer.data)

class AciditySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Acidity
        fields = ('id', 'style')
        