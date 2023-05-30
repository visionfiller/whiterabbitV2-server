"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from whiterabbitreports.views.helpers import dict_fetch_all


class VarietalRegionList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
          SELECT vr.id as varietal_region, v.name, r.country, r.location
            FROM whiterabbitapi_varietalregion vr
            JOIN whiterabbitapi_varietal v on v.id = vr.varietal_id
            JOIN whiterabbitapi_region r on r.id = vr.region_id 
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

           
            wines_by_country = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                varietal_region = {
                    "varietalregion_id": row ['varietal_region'],
                    "country" : row['country'],
                    "location": row['location'],
                    "name": row['name']
                    
                }
                
                # See if the gamer has been added to the games_by_user list already
                wine_dict = None
                for region_wine in wines_by_country:
                     if region_wine['country'] == row['country']:
                         wine_dict = region_wine
                
                
                if wine_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    wine_dict['varietal_regions'].append(varietal_region)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    wines_by_country.append({
                        "country": row['country'],
                        "varietal_regions": [varietal_region]
                    })
        
        # The template string must match the file name of the html template
        template = 'inventory/list_wines_country.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "region_varietal_list": wines_by_country
        }

        return render(request, template, context)
