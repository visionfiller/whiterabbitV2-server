from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Customer, VarietalRegion


class CustomerView(ViewSet):
    """customer view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            customer = Customer.objects.get(user=pk)  
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
             Response -- JSON serialized game instance
        """
        serializer = CreateCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
           
           
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        """delete varietal region"""
        customer= Customer.objects.get(pk=pk)
        customer.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'profile_picture','full_name']
class CustomerFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarietalRegion
        fields = ('id', 'varietal', 'region', 'body', 'dryness', 'acidity', 'is_favorite')
        depth=1
class CustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    favorites = CustomerFavoriteSerializer(many=True)
    class Meta:
        model = Customer
        fields = ('id', 'user', 'profile_picture', 'favorites', 'full_name')
        