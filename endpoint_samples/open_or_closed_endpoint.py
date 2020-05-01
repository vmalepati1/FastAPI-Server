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

# Get the current date and extract the week day number from it
current_date = datetime.date(datetime.now())
# Add 1 such that 0 = sunday, 1 = monday, 2 = tuesday, ...
day = current_date.weekday() + 1

# For the case of Sunday
if day > 6:
    day = 0

# No need to change this
# Authorization header information
headers = {"Authorization": "Bearer " + JWT_TOKEN}

# No need to change this
# Query parameters to pass to request
params = {
    'what_to_select': 'open_time, close_time',
    'which_table': 'company_timetable',
    'conditions_to_satisfy': 'Company_ID = ' + str(COMPANY_UUID) + ' AND weekday = ' + str(day)
}

# Make the request
response = requests.get(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

# If the request was successful
if response.status_code == 200:
    content = response.json()

    # Extract opening and closing times
    # Times are returned as floating point seconds since midnight
    open_time = content['rows'][0][0]
    close_time = content['rows'][0][1]

    # Get current seconds since midnight
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds

    is_open = (seconds >= open_time and seconds < close_time)
    print(is_open)
        
