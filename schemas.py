from pydantic import BaseModel, ConfigDict
from datetime import datetime


# LostItems
class LostItemBase(BaseModel):
    category_id: int
    name: str
    description: str = None
    lost_date: datetime = None
    location: str


class LostItemCreate(LostItemBase):
    pass


class LostItemUpdate(BaseModel):
    name: str = None
    description: str = None
    lost_date: datetime = None
    location: str = None


class LostItem(LostItemBase):
    id: int


# FoundtItems
class FoundItemBase(BaseModel):
    category_id: int
    name: str
    description: str = None
    found_date: datetime = None
    location: str


class FoundItemCreate(FoundItemBase):
    pass


class FoundItemUpdate(BaseModel):
    name: str = None
    description: str = None
    found_date: datetime = None
    location: str = None


class FoundItem(FoundItemBase):
    id: int


class CategoryCreate(BaseModel):
    name: str
    description: str = ""


class CategoryUpdate(BaseModel):
    name: str = None
    description: str = None


class CategoryRead(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
