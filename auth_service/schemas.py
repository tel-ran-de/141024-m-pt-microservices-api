from pydantic import BaseModel, ConfigDict
from datetime import datetime


#Users
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True