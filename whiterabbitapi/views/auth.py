from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from whiterabbitapi.models import Customer, Employee

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'auth_token': token.key,
            'user_id': authenticated_user.id,
            'is_staff': authenticated_user.is_staff
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
        request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        new_user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            is_staff = request.data['is_staff'])
        

        # Now save the extra info in the levelupapi_gamer table
        if request.data['is_staff']:
            whiterabbit_user = Employee.objects.create(
                user=new_user
            )
        else:
            whiterabbit_user=Customer.objects.create(
                profile_picture=request.data['profile_picture'],
                user=new_user)

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=whiterabbit_user.user)
        # Return the token to the client
        data = { 'auth_token': token.key,'valid': True,'user_id': whiterabbit_user.user,
            'is_staff': whiterabbit_user.user.is_staff}
        return Response(data)
    except Exception as ex:
        response = { 'message': ex.args[0] }
        return response