from PIL import Image
import requests
from io import BytesIO

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTM2OTU3LCJleHAiOjE1ODgxNDA1NTd9.vjb1FPKuRHEaTvtceiVAM5QTAULMUQGTVfYOwjy5tMw'

# Change to company name in app
COMPANY_NAME = 'SantaLucia'

# Web API host URL (change if needed)
# BASE_HOST_URL = 'http://127.0.0.1:8000'
BASE_HOST_URL = 'http://www.appspesa.it/api'
# URL where static images are stored on the server (change if needed)
# Need trailing slash
STATIC_FILE_HOST_URL = 'http://www.appspesa.it/img/'

# No need to change this
ENDPOINT_ROUTE = '/v1/query/read'

# No need to change this
# Authorization header information
headers = {"Authorization": "Bearer " + JWT_TOKEN}

# No need to change this
# Query parameters to pass to request
# Find the splash image url by matching the company name
params = {
    'what_to_select': 'splash_url',
    'which_table': 'company',
    'conditions_to_satisfy': "Company_Name = '" + COMPANY_NAME + "'"
}

# Make the request
response = requests.get(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

# If the request was successful, get the splash image path on the server and download the image
if response.status_code == 200:
    content = response.json()

    SPLASH_IMAGE_PATH = content['rows'][0][0]

    # Get entire path to image on the server
    splash_image_url = STATIC_FILE_HOST_URL + SPLASH_IMAGE_PATH

    # Download image
    response = requests.get(splash_image_url)
    img = Image.open(BytesIO(response.content))

    # Show image
    img.show()

    
    
