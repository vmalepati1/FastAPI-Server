from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTgzMjg5LCJleHAiOjE1ODgxODY4ODl9.PK1gZswB1_dzV13iZ6YCyOES4bCKCh00vvnho8gSLjM'

# Change to the user (not operator) ID who is managing the cart
USER_ID = 4

def make_read_request(what_to_select, table, conditions):
    # Web API host URL (change if needed)
    # BASE_HOST_URL = 'http://127.0.0.1:8000'
    BASE_HOST_URL = 'http://www.appspesa.it/api'
    # No need to change this
    ENDPOINT_ROUTE = '/v1/query/read'

    # No need to change this
    # Authorization header information
    headers = {"Authorization": "Bearer " + JWT_TOKEN}

    # No need to change this
    # Query parameters to pass to request
    params = {
        'what_to_select': what_to_select,
        'which_table': table,
        'conditions_to_satisfy': conditions
    }

    # Make request and return the response
    return requests.get(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

# Get all cart notes for carts that were confirmed orders for the user
r = make_read_request('cart_note', 'cart', 'User_ID = ' + str(USER_ID) + ' AND Confirmed = 1')

# If the request was successful
if r.status_code == 200:
    content = r.json()

    # Flatten list of cart note messages
    list_of_messages = [item for sublist in content['rows'] for item in sublist]

    # Print list of messages for user
    print(list_of_messages)

        
