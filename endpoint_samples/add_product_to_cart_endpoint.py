from PIL import Image
import requests
from io import BytesIO
import datetime

# Company UUID provided to you
COMPANY_UUID = 9

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTk1MjA1fQ.A6QVTjGLaYAwxOYN0khYxls1_xf6hHHb4VSg5nqZsVc'

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

def make_insert_request(table, values, column_names):
    # Web API host URL (change if needed)
    # BASE_HOST_URL = 'http://127.0.0.1:8000'
    BASE_HOST_URL = 'http://www.appspesa.it/api'
    # No need to change this
    ENDPOINT_ROUTE = '/v1/query/insert'

    # No need to change this
    # Authorization header information
    headers = {"Authorization": "Bearer " + JWT_TOKEN}

    # No need to change this
    # Query parameters to pass to request
    params = {
        'table_name': table,
        'values': values,
        'column_names': column_names
    }

    # Make request and return the response
    return requests.post(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

# Find cart that hasn't been confirmed yet (the one that is being edited currently)
r = make_read_request('id', 'cart', 'Confirmed = 0')

if r.status_code == 200:
    # Retrieve cart id
    cart_id = r.json()['rows'][0][0]

    # Change to the id of the product the user selected
    PRODUCT_ID = 1
    # Change to quantity user selected
    QUANTITY = 100

    date_placed = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    r = make_insert_request('cart_detail', "{0}, {1}, {2}, {3}, '{4}'"
                            .format(cart_id, PRODUCT_ID, COMPANY_UUID, QUANTITY, date_placed),
                            'Cart_ID, Prodcut_ID, Company_ID, Quantity, DatePlaced')

    if r.status_code == 200:
        print('Successfully added product to cart')
    else:
        # Error handling (maybe retry update)
        print('Could not add product to cart')
