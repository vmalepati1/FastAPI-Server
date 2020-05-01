import requests

# This endpoint will return the JWT token that is needed to make future requests
# The returned JWT token will be passed in the authorization header of future requests

# Operator credentials to access database
OPERATOR_USERNAME = 'test'
OPERATOR_PASSWORD = 'hello123'

# Web API host URL (change if needed)
BASE_HOST_URL = 'http://127.0.0.1:8000'
# BASE_HOST_URL = 'http://www.appspesa.it/api'

# No need to change this
ENDPOINT_ROUTE = '/v1/auth/get_token'

# Make the request
response = requests.post(BASE_HOST_URL + ENDPOINT_ROUTE, data={'username': OPERATOR_USERNAME, 'password': OPERATOR_PASSWORD})

# If the request was successful, print the returned JWT token
if response.status_code == 200:
    content = response.json()

    # Store this token temporarily on your app so that you can make future requests to other endpoints
    # It will eventually expire
    jwt_token = content['access_token']

    print(jwt_token)
