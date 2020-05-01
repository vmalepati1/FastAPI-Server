from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTgzMjg5LCJleHAiOjE1ODgxODY4ODl9.PK1gZswB1_dzV13iZ6YCyOES4bCKCh00vvnho8gSLjM'

# Change to the company UUID that was provided to you
COMPANY_UUID = 9

# URL where static images are stored on the server (change if needed)
# Need trailing slash
STATIC_FILE_HOST_URL = 'http://www.appspesa.it/img/'

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

r = make_read_request('Category_ID', 'category_company_assignment', 'Company_ID = ' + str(COMPANY_UUID))

# If the request was successful
if r.status_code == 200:
    content = r.json()

    # List of category names for the company
    cat_names = []
    # List of category icons for the company
    cat_icons = []
    # Is the category a child of another category (may want to display differently
    # in UI)
    cat_is_child = []

    for cat_id in content['rows']:
        cat_id = cat_id[0]

        # Extract name, icon url, and parent id based on category id
        r = make_read_request('Category_Name, ICON_URL, Parent_Category_ID',
                              'categories', 'Category_ID = ' + str(cat_id))

        # print(r)
        if r.status_code == 200:
            # Insert data into lists
            cat_data = r.json()
            
            cat_names.append(cat_data['rows'][0][0])

            ICON_IMAGE_PATH = cat_data['rows'][0][1]

            # Get entire path to image on the server
            icon_image_url = STATIC_FILE_HOST_URL + ICON_IMAGE_PATH

            # Download image
            response = requests.get(icon_image_url)
            img = Image.open(BytesIO(response.content))
            
            cat_icons.append(img)
            cat_is_child.append(cat_data['rows'][0][2] != None)

    # Print lists
    # cat_icons contains list of image objects, so cannot print
    print(cat_names)
    print(cat_is_child)

        
