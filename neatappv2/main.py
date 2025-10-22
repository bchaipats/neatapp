from fastapi import FastAPI
from .api import restaurant

app = FastAPI(title="Neatapp v2 API")

# Register routers
app.include_router(restaurant.router, prefix="/restaurants", tags=["restaurants"])


@app.get("/")
def read_root():
    return {"msg": "Welcome to Neatapp v2!"}