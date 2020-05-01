from PIL import Image
import requests
from io import BytesIO
import datetime

# Company UUID provided to you
COMPANY_ID = 9

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

# Find all products in product table
r = make_read_request('weekday, open_time, close_time', 'company_timetable', 'Company_ID = '
                      + str(COMPANY_ID))

# If the request was successful
if r.status_code == 200:
    timings = r.json()['rows']

    # Convert time since midnight to normal printable string
    for timing in timings:
        midnight = datetime.datetime(1, 1, 1, hour=0, minute=0, second=0)
        
        opd = datetime.timedelta(seconds=timing[1])
        cld = datetime.timedelta(seconds=timing[2])
        
        timing[1] = (midnight + opd).strftime('%H:%M:%S')
        timing[2] = (midnight + cld).strftime('%H:%M:%S')

    # Print timetable
    print(timings)
