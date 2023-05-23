from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whiterabbitapi.models import Employee


class EmployeeView(ViewSet):
    """customer view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
             Response -- JSON serialized game instance
        """
        serializer = CreateEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
           
           
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        """delete varietal region"""
        employee= Employee.objects.get(pk=pk)
        employee.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user','full_name']
class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Employee
        fields = ('id', 'user', 'full_name')
        