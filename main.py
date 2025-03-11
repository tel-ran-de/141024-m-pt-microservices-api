from fastapi import FastAPI, Depends, HTTPException
from routers.lost_items import router as lost_item_router
from routers.found_items import router as found_items_router


app = FastAPI()
app.include_router(lost_item_router, prefix="/lost_items", tags=["lostItems"])
app.include_router(found_items_router, prefix="/found_items", tags=["foundItems"])


@app.get("/")
def read_root():
    return {"message": "Welcome LostAndFound API"}
