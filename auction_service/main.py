from fastapi import FastAPI, Depends, HTTPException
from routers.auctions import router as auction_router
from routers.bids import router as bid_router

app = FastAPI(
    title="Auction API",
    version="1.0.0",
    openapi_url="/openapi.json",  # внутренний путь, без префикса
    docs_url="/docs",             # внутренний путь, без префикса
    redoc_url="/redoc",
    root_path="/auction",             # внешний префикс
    root_path_in_servers=True     # включаем генерацию серверов с префиксом
)
app.include_router(auction_router, prefix="/auctions", tags=["Auctions"])
app.include_router(bid_router, prefix="", tags=["Bids"])
# app.include_router(found_items_router, prefix="/found_items", tags=["foundItems"])
# app.include_router(categories_router, prefix="/categories", tags=["categories"])


@app.get("/")
def read_root():
    return {"message": "Welcome Auctions API"}
