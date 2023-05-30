"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from whiterabbitreports.views.helpers import dict_fetch_all


class CustomerFavoriteList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT  u.first_name || ' ' || u.last_name AS full_name, u.id as user_id,f.id as favorite_id,r.country || ' ' || v.name as varietal_region
            FROM whiterabbitapi_favorite f
            JOIN whiterabbitapi_customer c ON c.id = f.customer_id
            JOIN auth_user u ON u.id = c.user_id
            JOIN whiterabbitapi_varietalregion vr ON vr.id = f.varietal_region_id
            JOIN whiterabbitapi_varietal v on v.id = vr.varietal_id
            JOIN whiterabbitapi_region r on r.id = vr.region_id


            
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

           
            favorites_by_customer = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                favorite = {
                    "user_id": row ['user_id'],
                    "varietal_region" : row['varietal_region']
                    
                }
                
                # See if the gamer has been added to the games_by_user list already
                customer_dict = None
                for customer_favorite in favorites_by_customer:
                     if customer_favorite['user_id'] == row['user_id']:
                         customer_dict = customer_favorite
                
                
                if customer_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    customer_dict['favorites'].append(favorite)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    favorites_by_customer.append({
                        "user_id": row['user_id'],
                        "full_name": row['full_name'],
                        "favorites": [favorite]
                    })
        
        # The template string must match the file name of the html template
        template = 'customers/list_with_favorites.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "customer_favorite_list": favorites_by_customer
        }

        return render(request, template, context)
