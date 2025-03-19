from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Модель для данных пользователя в JWT
class TokenData(BaseModel):
    username: str | None = None


class TagBase(BaseModel):
    """
    Базовая модель для тега.
    Здесь может быть только имя, если мы не планируем других полей.
    """
    name: str


class TagCreate(TagBase):
    """
    Для создания/обновления тега. Пока ничего не добавляем, но
    если захотим запретить пустые строки, можно прописать валидаторы.
    """
    pass


class TagUpdate(BaseModel):
    """
    Если нужно частичное обновление (patch), можно добавить поля:
    name: Optional[str] = None
    """
    name: str | None = None


class TagRead(TagBase):
    """
    Возвращаемый при GET.
    Содержит id и name.
    """
    id: int

    class Config:
        from_attributes = True


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
    # Возвращаем список тегов (при GET)
    tags: list[TagRead] = []

    class Config:
        from_attributes = True


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
    # Возвращаем список тегов (при GET)
    tags: list[TagRead] = []

    class Config:
        from_attributes = True


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
