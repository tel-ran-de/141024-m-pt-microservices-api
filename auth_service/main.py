from fastapi import FastAPI, Depends, HTTPException
from routers.users import router as users_router
from routers.auth import router as auth_router


app = FastAPI()
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def read_root():
    return {"message": "Welcome to AuthService API"}
