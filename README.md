# FastAPI-Server
This project is an API server that manages database queries and authorization across many users. The API is split into three routes: authorization, query, and info. These routes will be explained in detail.

## Getting Started - Server Side
### Prerequisites
   1. First start by installing all the dependencies listed in `requirements.txt` using `pip` or a virtual environment.
   2. Before deploying the API, you must configure the server settings in `server_config.yml`.
      - Note that the settings in `server_config.yml` can be changed while the server is running. The server will check for any changes to the config file and reload them if necessary, so there is no need to restart the server when the config file is changed.
      - Under key `mysql`:
         - `host`, `port`, `username`, `password`, and `db` will specify the credentials needed to connect to your MySQL database.
      - Under key `server_settings`:
         - `jwt_key`: a secret key that will be used to sign the JWT tokens that will be returned by the authorization route on the server side
         - `token_expiry_minutes`: The amount of time in minutes that a JWT token produced by the authorization route will last. If set to a negative number, JWT tokens will not expire. **Setting a valid expiry time is recommended in case a token is stolen or lost.**
### Development/Testing Deployment
   - If you need to just run the server on your local machine for testing/development purposes, you can run either of the following commands:
      - `uvicorn main:app --reload`
         - Running this command will enable you to make changes in the code and see the server update in real-time
      - `python main.py`
### Production Deployment
   - The API is run on [Uvicorn](https://www.uvicorn.org/deployment/), an ASGI server. In the future, the project will be transitioned into a Docker Swarm mode cluster with Traefik and HTTPS or Gunicorn.
   - Since usernames and passwords are transmitted between the client and the API, it is recommended that Uvicorn be run with HTTPS
      - So first, a certificate and a private key are required
      - Get a certificate and key for the server website using [Let's Encrypt](https://letsencrypt.org/)
      - Specify the certificate and key file locations when running Uvicorn using the `--ssl-keyfile` and `--ssl-certfile` flags:
         - `uvicorn main:app --port 5000 --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem`
         - Note: Do not use the `--reload` flag in production
      - Alternatively, Nginx may be used as a proxy between the client and Uvicorn. This can reduce the load on the application servers. See [here](https://avilpage.com/2018/05/deploying-scaling-django-channels.html) for an example on how to set up a Nginx proxy for a web API.
      - Running Uvicorn with HTTPS will allow the API server to be hosted in the web domain certified by your SSL certificate
## Using the API - Client Side
### Accessing Documentation
Using the API is simple and straightforward. You must ask the API provider for the website on which the server is hosted. Typically this website will look something like this: https://api.domain_name.com. The domain name will depend on the API Server provider. Using this base URL, you can then make requests to the Web API and access the interactive docs. To access the API documentation, you can add `/docs` to the base URL for the SwaggerUI style docs or you can alternatively add `/redoc` for the ReDoc docs. If you want to access the interactive docs on your own, you can start the server on localhost using the steps in "Development/Testing Deployment" and then access the docs by going to http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc. Accessing the docs and making requests to the API will require that you, as the client, use the HTTPS/TLS protocol. Documentation for the API is also located in the docs folder of this repository as static (not interactive) PDF files for both the SwaggerUI and Redoc documentation styles. Note that the PDF docs in this repository provide HTTP requests that assume the API server is running on localhost, which is most likely not the case. Replace the http://127.0.0.1:8000 in each curl command and request URL with the base URL given by your API server provider.
### Making Requests
Requests will be made to the base URL followed by the route. For example, if the server is running locally, a POST request could be sent to http://127.0.0.1:8000/v1/auth/get_token (`/v1/auth/` is the route and `get_token` is the endpoint). Below we will discuss how to make HTTP requests to the API server.
#### 1. First Step: Authorize the User
   - Before any requests can be made to the API Server, the client user must be authenticated.
   - To authenticate a user, his or her `username` and `password` must be sent to the `/v1/auth/get_token` endpoint. The server will check the `username` and `password` and return a JWT token containing the user's database privileges. **This token will be passed in the authorization header of subsequent requests to verify the user.** The token will expire after some time. As the client, you must save the token temporarily so that you can make future requests to the server.
   - The `username` and `password` of the user must be passed using OAuth2 password flow
      - For example, say `username` is `test` and `password` is `hello123`. The request sent to http://127.0.0.1:8000/v1/auth/get_token will look like this:
         - `curl -X POST "http://127.0.0.1:8000/v1/auth/get_token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=&username=test&password=hello123&scope=&client_id=&client_secret="`
         - And, assuming `username` and `password` are valid, the server would return the JWT token like so:
            ```
            {
              "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
              "token_type": "bearer"
            }
            ```
   - Regarding security, sending `username` and `password` as plaintext is safe as the connection between the client and the server API is secured with HTTPS
   - Note that the authentication process specified above is fully documented in the API docs. Please refer to the API docs if you have further questions.
   - After authenticating the user, requests can be made to any of the other routes in the API server using the JWT token
### 2. Second Step: Make Requests to other Routes
   - Besides the authorization route, there are two other routes
   - When using these two routes, you must pass the JWT token from the previous step in the authorization header
      - For example, say you are sending a request to create a table using the `create` endpoint. Your request will look like this:
         - `curl -X POST "http://127.0.0.1:8000/v1/query/create?table_name=categories&field_defs=Category_ID%20int%2811%29%2C%20Category_Name%20varchar%28500%29" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"`
         - **Notice how the token from step 1 was passed in**
      - If you do not pass a token or the token is invalid, you will get an unauthorized 401 Error.
   - `/v1/query/` Database Query Route
      - This route is used to make queries to the database. Please see the API docs for all the endpoints in this route
      - **Note: For security purposes, when creating a user (adding an operator) as a record in the database, you must encrypt their password when using the `insert` endpoint. You must use the [bcrypt](https://github.com/pyca/bcrypt) algorithm. In other words, all passwords stored in the database must be encrypted using bcrypt. The authorization route will compare the bcrypt hash in the database with the password passed in from the client to generate the JWT token.**
   - `/v1/info/' General Information Route
      - This route is used to retrieve general information from the server. A user can find out what database privileges he or she has by passing in his or her JWT token. This route is used to make queries to the database. Please see the API docs for all the endpoints in this route
## Tests: to come
## Built With
   - [FastAPI](https://fastapi.tiangolo.com/)
   - [Uvicorn](https://www.uvicorn.org/)
