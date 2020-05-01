from PIL import Image
import requests
from io import BytesIO
from datetime import datetime

# Get delivery date of cart order

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTk1MjA1fQ.A6QVTjGLaYAwxOYN0khYxls1_xf6hHHb4VSg5nqZsVc'

# Change to the cart that the user is editing
# You could find this cart with the user's id by searching for a cart
# that matches the user id and also has confirmed = 0 (meaning the cart
# is still being edited)
# Could also search by operator id
CART_ID = 1

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

def convertSQLDateTimeToDatetime(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

# Retrieve the bool value for if cart order has been delivered and can be retired
r = make_read_request('DateDelivery', 'cart', 'id = ' + str(CART_ID))

# If the request was successful
if r.status_code == 200:
    content = r.json()

    # Retrieve delivery date information
    date = content['rows'][0][0]
    timestamp = convertSQLDateTimeToDatetime(date)

    delivery_time = timestamp.time()

    print(delivery_time)

    

    
