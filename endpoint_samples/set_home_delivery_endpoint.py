from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTk1MjA1fQ.A6QVTjGLaYAwxOYN0khYxls1_xf6hHHb4VSg5nqZsVc'

# Change to the cart that the user is editing
# You could find this cart with the user's id by searching for a cart
# that matches the user id and also has confirmed = 0 (meaning the cart
# is still being edited)
# Could also search by operator id
CART_ID = 1

def make_update_request(table, set_statements, condition):
    # Web API host URL (change if needed)
    BASE_HOST_URL = 'http://www.appspesa.it/api'
    # BASE_HOST_URL = 'http://127.0.0.1:8000'
    # No need to change this
    ENDPOINT_ROUTE = '/v1/query/update'

    # No need to change this
    # Authorization header information
    headers = {"Authorization": "Bearer " + JWT_TOKEN}

    # No need to change this
    # Query parameters to pass to request
    params = {
        'table_name': table,
        'set_statements': set_statements,
        'where_condition': condition
    }

    # Make request and return the response
    return requests.put(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

is_home_delivery = False

# Update the home delivery flag
r = make_update_request('cart', 'HomeDelivery = ' + str(int(is_home_delivery)),
                        'id = ' + str(CART_ID))

# If the request was successful
if r.status_code == 200:
    print('Successfully updated home delivery availability')
else:
    # Error handling (maybe retry update)
    print('Could not update home delivery availability')
