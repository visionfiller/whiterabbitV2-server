from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User


class UserView(ViewSet):
    """customer view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        users = User.objects.all()
        email = request.query_params.get('email', None)
        
        if email is not None:
            users = users.filter(email=email)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
   
    # def destroy(self, request, pk):
    #     """delete varietal region"""
    #     customer= Customer.objects.get(pk=pk)
    #     customer.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)  
    def update(self, request, pk):
            """Handle PUT requests for a game

            Returns:
                Response -- Empty body with 204 status code
            """
            user = User.objects.get(pk=pk)
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            user.set_password(request.data["password"])
            user.username = request.data["username"]
            user.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')
        