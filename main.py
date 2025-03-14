from fastapi import FastAPI, Depends, HTTPException
from routers.lost_items import router as lost_item_router
from routers.found_items import router as found_items_router
from routers.categories import router as categories_router
from routers.tags import router as tags_router
from routers.users import router as users_router


app = FastAPI()
app.include_router(lost_item_router, prefix="/lost_items", tags=["lostItems"])
app.include_router(found_items_router, prefix="/found_items", tags=["foundItems"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(tags_router, prefix="/tags", tags=["tags"])
app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome LostAndFound API"}
