from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTkxMDE1LCJleHAiOjE1ODgxOTQ2MTV9.eSCSKe31iB_zXndEirbnBZV6Vu1cJYnA1fsdHc3C-T8'

# Change to the cart that the user is editing
# You could find this cart with the user's id by searching for a cart
# that matches the user id and also has confirmed = 0 (meaning the cart
# is still being edited)
# Could also search by operator id
CART_ID = 1

def make_read_request(what_to_select, table, conditions):
    # Web API host URL (change if needed)
    BASE_HOST_URL = 'http://127.0.0.1:8000'
    # BASE_HOST_URL = 'http://www.appspesa.it/api'
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

# Retrieve the bool value for if home delivery for the order is available
r = make_read_request('HomeDelivery', 'cart', 'id = ' + str(CART_ID))

# If the request was successful
if r.status_code == 200:
    content = r.json()

    home_delivery_available = bool(content['rows'][0][0])

    # Print whether home delivery is available
    print(home_delivery_available)
