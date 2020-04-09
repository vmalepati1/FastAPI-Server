from fastapi import FastAPI

import os
from routes.v1 import auth, query

app = FastAPI(
  title="MySQL API Server",
  description="Allows users to access a database with access management",
  version="0.0.1"
)

app.include_router(
  auth.router,
  prefix='/v1/auth',
  tags=["Authentication"]
)

app.include_router(
  query.router,
  prefix='/v1/query',
  tags=["Query"]
)

# Testing only
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
