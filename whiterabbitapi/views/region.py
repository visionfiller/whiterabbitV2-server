"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Region


class RegionView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            region = Region.objects.get(pk=pk)
            serializer = RegionSerializer(region)
            return Response(serializer.data)
        except Region.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)
    def create(self, request):
        """create region"""
        serializer = CreateRegionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        """delete varietal region"""
        region= Region.objects.get(pk=pk)
        region.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
class CreateRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'location', 'geo_code_city', 'country']
class RegionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Region
        fields = ('id', 'location', 'geo_code_city', 'country')
        