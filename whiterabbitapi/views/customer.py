from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Customer, VarietalRegion, Message
from rest_framework.decorators import action
from django.contrib.auth.models import User


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
    def update(self, request, pk):
            """Handle PUT requests for a game

            Returns:
                Response -- Empty body with 204 status code
            """
            customer = Customer.objects.get(user=pk)
            customer.profile_picture = request.data["profile_picture"]
            customer.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['post'], detail=True)       
    def message(self, request, pk):
        user= User.objects.get(pk=request.auth.user.id)
        receiver = Customer.objects.get(user=pk)
        sender = Customer.objects.get(user=user.id)
        
        message = Message.objects.create(receiver=receiver, sender=sender, body=request.data['body'])
        receiver.received_messages.add(message)
        sender.sent_messages.add(message)
        return Response({'message': 'Message Sent!'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def deletemessage(self, request, pk):
       
        message = Message.objects.get(pk=request.data['id'])
        message.delete()
        return Response({'message': 'Message Deleted!'}, status=status.HTTP_204_NO_CONTENT)
class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'profile_picture']
class CustomerFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarietalRegion
        fields = ('id', 'varietal', 'region', 'body', 'dryness', 'acidity', 'is_favorite')
        depth=1
class CustomerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'body', 'formatted_date')
class CustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    favorites = CustomerFavoriteSerializer(many=True)
    sent_messages = CustomerMessageSerializer(many=True)
    received_messages = CustomerMessageSerializer(many=True)
    class Meta:
        model = Customer
        fields = ('id', 'user', 'profile_picture', 'favorites','received_messages','sent_messages', 'full_name')
        