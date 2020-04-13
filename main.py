from fastapi import FastAPI

import os
from routes.v1 import auth, query, info

app = FastAPI(
  title="MySQL API Server",
  description="Allows users to access a database with access management",
  version="0.0.1"
)

# Establish authorization route
app.include_router(
  auth.router,
  prefix='/v1/auth',
  tags=["Authentication"]
)

# Establish query route for database queries
app.include_router(
  query.router,
  prefix='/v1/query',
  tags=["Query"]
)

# Establish info route for general info
app.include_router(
  info.router,
  prefix='/v1/info',
  tags=["Info"]
)

# Testing only: will automatically run the server on localhost with 
# default settings. Use by typing: python main.py
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)
