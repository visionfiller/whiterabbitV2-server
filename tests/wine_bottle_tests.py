import json
from rest_framework import status
from rest_framework.test import APITestCase
from whiterabbitapi.models import WineBottle, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BottleTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'varietals', 'region', 'winetypes', 'acidities', 'bodies', 'drynesses']

    def setUp(self):
       
        self.user = User.objects.first()
        self.user2 = User.objects.create(first_name="Poppy")
        token = Token.objects.get(user=self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.customer2= Customer.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_wine_bottles(self):
        response = self.client.get('/winebottles')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), WineBottle.objects.count())

    def test_create_wine_bottle(self):
        """
        Ensure we can create a new wine bottle.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        varietal_url = "/varietalregions"
        varietal_data = {
            "varietal": 1,
            "region": 2,
            "body": 2,
            "acidity": 3,
            "dryness": 2,
        }
        response = self.client.post(varietal_url, varietal_data, format='json')

        data = {
            "name": "Les Petits Fers",
            "vintage": 2020,
            "varietal_region": 1,
            "image": "testtest.com/jpeg",
            "link": "testtest.com"
        }

        # Initiate request and store response
        url = "/winebottles"
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Les Petits Fers")
        self.assertEqual(json_response["vintage"], 2020)
        self.assertEqual(json_response["varietal_region"], 1)
        self.assertEqual(json_response["image"], "testtest.com/jpeg")
        self.assertEqual(json_response["link"], "testtest.com")

    def test_delete_wine_bottle(self):
        # Initiate request and store response
        varietal_url = "/varietalregions"
        varietal_data = {
            "varietal": 1,
            "region": 2,
            "body": 2,
            "acidity": 3,
            "dryness": 2,
        }
        response = self.client.post(varietal_url, varietal_data, format='json')

        data = {
            "name": "Les Petits Fers",
            "vintage": 2020,
            "varietal_region": 1,
            "image": "testtest.com/jpeg",
            "link": "testtest.com"
        }

        # Initiate request and store response
        url = "/winebottles"
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
      
        wine_bottle = WineBottle.objects.first()
        response = self.client.delete(f'/winebottles/{wine_bottle.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
