import json
from rest_framework import status
from rest_framework.test import APITestCase
from whiterabbitapi.models import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CustomerTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'varietals', 'region', 'winetypes', 'acidities', 'bodies', 'drynesses']

    def setUp(self):
       
        self.user = User.objects.first()
        self.user2 = User.objects.create(first_name="Poppy")
        token = Token.objects.get(user=self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.customer2= Customer.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_customers(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Customer.objects.count())
    def test_edit_customer(self):
        customer = self.customer
        data = {
            "profile_picture": "testeset"
        
        }
        response = self.client.put(f'/customers/{customer.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        customer_updated = Customer.objects.get(pk=customer.id)
        self.assertEqual(customer_updated.profile_picture, data['profile_picture'])
    def test_delete_customer(self):
        # Initiate request and store response
        customer = self.customer
        response = self.client.delete(f'/customers/{customer.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_message(self):
        customer=self.customer
        customer2=self.customer2

         
        data = {
            "sender" :customer.user.id,
            "receiver": customer2.user.id,
            "body": "test"
    }
        response = self.client.post(f'/customers/{customer2.user.id}/message', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   
       
