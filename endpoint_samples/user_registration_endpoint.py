from PIL import Image
import requests
from io import BytesIO
import datetime
import bcrypt

# Some sample token. Instead replace with the token returned by authentication endpoint
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWFkIjoxLCJhY3AiOm51bGwsInRicCI6bnVsbCwiaWF0IjoxNTg4MTk1MjA1fQ.A6QVTjGLaYAwxOYN0khYxls1_xf6hHHb4VSg5nqZsVc'

def make_insert_request(table, values, column_names):
    # Web API host URL (change if needed)
    # BASE_HOST_URL = 'http://127.0.0.1:8000'
    BASE_HOST_URL = 'http://www.appspesa.it/api'
    # No need to change this
    ENDPOINT_ROUTE = '/v1/query/insert'

    # No need to change this
    # Authorization header information
    headers = {"Authorization": "Bearer " + JWT_TOKEN}

    # No need to change this
    # Query parameters to pass to request
    params = {
        'table_name': table,
        'values': values,
        'column_names': column_names
    }

    # Make request and return the response
    return requests.post(BASE_HOST_URL + ENDPOINT_ROUTE, headers=headers, params=params)

class RegistrationForm:
    def __init__(self):
        # Get following values from the form in the UI
        self.First_name = 'Hello'
        self.Last_name = ''
        self.Mobile_num = ''
        self.Email = ''
        self.Username = ''
        self.Password = 'test'
        self.City = ''
        self.Address1 = ''
        self.Address2 = ''
        self.Address_num = ''
        self.zip_code = ''
        self.Address_note = ''
        self.invoice_name = ''
        self.invoice_cf = ''
        self.invoice_piva = ''
        self.invoice_address = ''
        self.invoice_addrnum = ''
        self.invoice_City = ''
        self.invoice_zip = ''
        self.invoice_Province = ''

rf = RegistrationForm()

# Must encrypt password using bcrypt before inserting into database

salt = bcrypt.gensalt()
rf.Password = bcrypt.hashpw(rf.Password.encode(), salt).decode("utf-8")

values = "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}'".format(
        rf.First_name, rf.Last_name, rf.Mobile_num, rf.Email, rf.Username, rf.Password,
        rf.City, rf.Address1, rf.Address2, rf.Address_num, rf.zip_code, rf.Address_note,
        rf.invoice_name, rf.invoice_cf, rf.invoice_piva, rf.invoice_address, rf.invoice_addrnum,
        rf.invoice_City, rf.invoice_zip, rf.invoice_Province)

r = make_insert_request('user', values, ','.join(rf.__dict__.keys()))

if r.status_code == 200:
    print('Successfully registered user')
else:
    # Error handling (maybe retry update)
    print('Could not register user')
