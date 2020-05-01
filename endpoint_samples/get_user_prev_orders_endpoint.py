from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTkxMDE1LCJleHAiOjE1ODgxOTQ2MTV9.eSCSKe31iB_zXndEirbnBZV6Vu1cJYnA1fsdHc3C-T8'

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

# Get all cart ids for orders that were confirmed by the user
r = make_read_request('id', 'cart', 'User_ID = ' + str(USER_ID) + ' AND Confirmed = 1')

# If the request was successful
if r.status_code == 200:
    content = r.json()

    # List of tuples with order details (Prodcut_ID, Company_ID, Quantity, DatePlaced)
    # You can then use Product_ID to find product name by doing a simple search in the product table
    # Same for Company_ID
    order_list = []

    for c_id in content['rows']:
        c_id = c_id[0]

        # Take the cart id and retrieve details of order

        r = make_read_request('Prodcut_ID, Company_ID, Quantity, DatePlaced', 'cart_detail',
                              'Cart_ID = ' + str(c_id))

        if r.status_code == 200:
            order_details_l = r.json()['rows']

            # If the order detail search returned empty, the cart order may not have
            # been placed correctly (server-side error)
            if len(order_details_l) >= 1:
                order_list.append(order_details_l[0])

    # Print order detail list
    print(order_list)            
            
        
