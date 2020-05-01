from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTk1MjA1fQ.A6QVTjGLaYAwxOYN0khYxls1_xf6hHHb4VSg5nqZsVc'

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

# Find all products in product table
r = make_read_request('product_image', 'product_gallery', None)

# If the request was successful
if r.status_code == 200:
    image_urls = r.json()['rows']

    # List of images in gallery
    gallery_images = []

    # Convert product image URL to an actual image object
    for url in image_urls:
        ICON_IMAGE_PATH = url[0]

        # Get entire path to image on the server
        icon_image_url = STATIC_FILE_HOST_URL + ICON_IMAGE_PATH

        # Download image
        response = requests.get(icon_image_url)
        img = Image.open(BytesIO(response.content))

        gallery_images.append(img)

    print(gallery_images)
