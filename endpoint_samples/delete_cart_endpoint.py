from PIL import Image
import requests
from io import BytesIO

# UUID of cart to delete
CART_ID = 1

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTk1MjA1fQ.A6QVTjGLaYAwxOYN0khYxls1_xf6hHHb4VSg5nqZsVc'

def make_delete_request(table, conditions):
    # Web API host URL (change if needed)
    # BASE_HOST_URL = 'http://127.0.0.1:8000'
    BASE_HOST_URL = 'http://www.appspesa.it/api'
    # No need to change this
    ENDPOINT_ROUTE = '/v1/query/delete'

    # No need to change this
    # Authorization header information
    headers = {"Authorization": "Bearer " + JWT_TOKEN}

    # No need to change this
    # Query parameters to pass to request
    params = {
        'table_name': table,
        'where_condition': conditions
    }

    # Make request and return the response
    return requests.delete(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)


r = make_delete_request('cart', 'id = ' + str(CART_ID))

if r.status_code == 200:
    print('Successfully deleted cart')
else:
    # Error handling (maybe retry delete)
    print('Could not delete cart')
