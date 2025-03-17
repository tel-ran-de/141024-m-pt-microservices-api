from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.users import router as users_router


app = FastAPI(
    title="AuthService API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/auth",
    root_path_in_servers=True
)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to AuthService API"}
