import json
from rest_framework import status
from rest_framework.test import APITestCase
from whiterabbitapi.models import VarietalRegion, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class VarietalRegionTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'varietals', 'region', 'winetypes', 'acidities', 'bodies', 'drynesses']

    def setUp(self):
       
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_varietal_region(self):
        """
        Ensure we can create a new game.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/varietalregions"

        # Define the request body
        data = {
            "varietal": 1,
            "region": 2,
            "body": 2,
            "acidity": 3,
            "dryness": 2,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["varietal"], 1)
        self.assertEqual(json_response["region"], 2)
        self.assertEqual(json_response["body"], 2)
        self.assertEqual(json_response["acidity"], 3)
        self.assertEqual(json_response["dryness"], 2)

    def test_edit_varietal_region(self):

        url = "/varietalregions"
        data = {
            "varietal": 1,
            "region": 2,
            "body": 2,
            "acidity": 3,
            "dryness": 2,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')
        varietal_region= VarietalRegion.objects.first()
        data2 = {
            "varietal": 1,
            "region": 2,
            "body": 3,
            "acidity": 3,
            "dryness": 2
        }
        response = self.client.put(f'/varietalregions/{varietal_region.id}', data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        varietal_region_updated = VarietalRegion.objects.get(pk=varietal_region.id)
        self.assertEqual(varietal_region_updated.body.id, data2['body'])

    def test_get_all_varietal_regions(self):
        response = self.client.get('/varietalregions')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), VarietalRegion.objects.count())

    def test_delete_varietal_region(self):
        url = "/varietalregions"
        data = {
            "varietal": 1,
            "region": 2,
            "body": 2,
            "acidity": 3,
            "dryness": 2,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')
        varietal_region= VarietalRegion.objects.first()
        response = self.client.delete(f'/varietalregions/{varietal_region.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_add_favorite(self):
        url = "/varietalregions"
        data = {
            "varietal": 1,
            "region": 2,
            "body": 2,
            "acidity": 3,
            "dryness": 2,
        }

        # Initiate request and store response
        response1 = self.client.post(url, data, format='json')
        varietal_region = VarietalRegion.objects.first()
        response = self.client.post(f'/varietalregions/{varietal_region.id}/favorite', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response2 = self.client.get(f'/varietalregions/{varietal_region.id}')
        json_response = json.loads(response2.content)
        self.assertEqual(json_response['is_favorite'], True)
