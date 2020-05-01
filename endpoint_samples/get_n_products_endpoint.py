import requests

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTgzMjg5LCJleHAiOjE1ODgxODY4ODl9.PK1gZswB1_dzV13iZ6YCyOES4bCKCh00vvnho8gSLjM'

# Cart ID may be fixed or you may have to find it by searching
# the table "cart" by the OperatorID (who is accessing the
# database records) and retrieving the entry's id
# Please let me know if you have any questions on how to do this
CART_ID = 1

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
# Find the splash image url by matching the company name
params = {
    'what_to_select': 'Quantity',
    'which_table': 'cart_detail',
    'conditions_to_satisfy': "Cart_ID = " + str(CART_ID)
}

# Make the request
response = requests.get(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

# If the request was successful, get the splash image path on the server and download the image
if response.status_code == 200:
    content = response.json()

    # Add up quantities
    n = 0

    for q in content['rows']:
        q = q[0]
        n += q

    # Print number of products in cart with ID Cart_ID
    print(n)
    
