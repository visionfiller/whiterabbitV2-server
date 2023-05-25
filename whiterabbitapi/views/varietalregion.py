"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from whiterabbitapi.models import VarietalRegion, Customer, Acidity, Dryness, Body


class VarietalRegionView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            varietal_region = VarietalRegion.objects.get(pk=pk)
            try:
                customer = Customer.objects.get(user=request.auth.user)
                varietal_region.is_favorite = varietal_region in customer.favorites.all()
            except Customer.DoesNotExist:
                varietal_region = VarietalRegion.objects.get(pk=pk)
                serializer = VarietalRegionSerializer(varietal_region)
                return Response(serializer.data)
            serializer = VarietalRegionSerializer(varietal_region)
            return Response(serializer.data)
        except VarietalRegion.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        varietal_regions = VarietalRegion.objects.all()
        
        varietal_id = request.query_params.get('varietal', None)
        wine_type_id = request.query_params.get('wine_type', None)
        if varietal_id is not None:
            varietal_regions = varietal_regions.filter(varietal=varietal_id)
        if wine_type_id is not None:
            varietal_regions = varietal_regions.filter(varietal__wine_type=wine_type_id)
        try:
            customer = Customer.objects.get(user=request.auth.user)
            for varietal_region in varietal_regions:
             varietal_region.is_favorite = varietal_region in customer.favorites.all()
            serializer = VarietalRegionSerializer(varietal_regions, many=True)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            varietal_regions = VarietalRegion.objects.all()
            varietal_id = request.query_params.get('varietal', None)
            wine_type_id = request.query_params.get('wine_type', None)
            if varietal_id is not None:
                varietal_regions = varietal_regions.filter(varietal=varietal_id)
            if wine_type_id is not None:
                varietal_regions = varietal_regions.filter(varietal__wine_type=wine_type_id)
            serializer = VarietalRegionSerializer(varietal_regions, many=True)
            return Response(serializer.data)

    def create(self, request):
            """Handle POST operations

            Returns
                Response -- JSON serialized game instance
            """
            serializer = CreateVarietalRegionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
           
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk):
            """Handle PUT requests for a game

            Returns:
                Response -- Empty body with 204 status code
            """
            varietal_region = VarietalRegion.objects.get(pk=pk)
            acidity = Acidity.objects.get(pk=request.data['acidity'])
            dryness = Dryness.objects.get(pk=request.data['dryness'])
            body = Body.objects.get(pk=request.data['body'])
            varietal_region.acidity = acidity
            varietal_region.dryness = dryness
            varietal_region.body = body
            varietal_region.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        """delete varietal region"""
        varietal_region = VarietalRegion.objects.get(pk=pk)
        varietal_region.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 

    @action(methods=['post'], detail=True)       
    def favorite(self, request, pk):
        varietal_region = VarietalRegion.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.auth.user)
        customer.favorites.add(varietal_region)
        return Response({'message': 'Favorited Added'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk):
            """Post request for a user to sign up for an event"""
            
            customer = Customer.objects.get(user=request.auth.user)
            varietal_region = VarietalRegion.objects.get(pk=pk)
            customer.favorites.remove(varietal_region)
            return Response({'message': 'Unfavorited'}, status=status.HTTP_204_NO_CONTENT)        

    # @action(methods=['delete'], detail=True)
    # def unsubscribe(self, request, pk):
    #     subscription = Subscription.objects.get(author=pk, follower=request.auth.user.id)
    #     subscription.delete()
    #     return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT) 
class CreateVarietalRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarietalRegion
        fields = ['id', 'varietal', 'region', 'body', 'dryness', 'acidity']
class VarietalRegionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = VarietalRegion
        fields = ('id', 'varietal', 'region', 'body', 'dryness', 'acidity', 'is_favorite')
        depth =1