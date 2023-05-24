"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Body


class BodyView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            body = Body.objects.get(pk=pk)
            serializer = BodySerializer(body)
            return Response(serializer.data)
        except Body.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        bodies = Body.objects.all()
        serializer = BodySerializer(bodies, many=True)
        return Response(serializer.data)

class BodySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Body
        fields = ('id', 'density')
        