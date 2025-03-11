from pydantic import BaseModel, ConfigDict
from datetime import datetime


# LostItems
class LostItemBase(BaseModel):
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
