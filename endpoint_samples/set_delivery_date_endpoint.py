from PIL import Image
import requests
from io import BytesIO
from datetime import datetime

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

def convertSQLDateTimeToDatetime(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

# First read in the original datetime
# We are only updating the date, not the time, so we need to extract the time from before
r = make_read_request('DateDelivery', 'cart', 'id = ' + str(CART_ID))
original_datetime = convertSQLDateTimeToDatetime(r.json()['rows'][0][0])

# Edit the original datetime with new date
new_datetime = original_datetime.replace(month=4, day=30)

# Update the home delivery flag
r = make_update_request('cart', "DateDelivery = '" + new_datetime.strftime('%Y-%m-%dT%H:%M:%S') + "'",
                        'id = ' + str(CART_ID))

print(r.content)

# If the request was successful
if r.status_code == 200:
    print('Successfully updated home delivery availability')
else:
    # Error handling (maybe retry update)
    print('Could not update home delivery availability')
