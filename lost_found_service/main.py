from fastapi import FastAPI
from routers.lost_items import router as lost_item_router
from routers.found_items import router as found_items_router
from routers.categories import router as categories_router
from routers.tags import router as tags_router
from faststream.rabbit.fastapi import RabbitRouter, Logger

router = RabbitRouter("amqp://guest:guest@rabbitmq:5672/")

app = FastAPI(
    title="LostAndFound API",
    version="1.0.0",
    openapi_url="/openapi.json",  # внутренний путь, без префикса
    docs_url="/docs",  # внутренний путь, без префикса
    redoc_url="/redoc",
    root_path="/api",  # внешний префикс
    root_path_in_servers=True  # включаем генерацию серверов с префиксом
)


@app.get("/send")
async def hello_http():
    await router.broker.publish("Hello, Rabbit!", queue="test")
    return "Message sent"


app.include_router(lost_item_router, prefix="/lost_items", tags=["lostItems"])
app.include_router(found_items_router, prefix="/found_items", tags=["foundItems"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(tags_router, prefix="/tags", tags=["tags"])
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to LostAndFound API"}
