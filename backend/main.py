from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import event, user, market

app = FastAPI()

app.include_router(event.router)
app.include_router(user.router)
app.include_router(market.router)

# set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods（GET、POST..）
    allow_headers=["*"],  # allow all head
)


@app.get("/")
def read_root():
    return {"Hello": "Welcome"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q":q}

# @app.get("/items/{item_id}")
# def create_event(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q":q}


    
    