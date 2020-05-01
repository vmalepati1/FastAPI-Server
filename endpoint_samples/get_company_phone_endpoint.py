from datetime import datetime
import requests

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTc5MzEzLCJleHAiOjE1ODgxODI5MTN9.bfz8-qf51-bfukz-LEm7PRs-RxBakBrNQl3yARtIz_M'

# Change to the company UUID that was provided to you
COMPANY_UUID = 9

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
    'what_to_select': 'Phone1',
    'which_table': 'company',
    'conditions_to_satisfy': 'Company_ID = ' + str(COMPANY_UUID)
}

# Make the request
response = requests.get(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

# If the request was successful
if response.status_code == 200:
    content = response.json()

    # Extract phone number
    phone_num = content['rows'][0][0]

    print(phone_num)

        
