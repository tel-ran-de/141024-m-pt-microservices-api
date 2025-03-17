from sqlalchemy import Column, Integer, String, DateTime, Text, Table, ForeignKey, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


# Ассоциативная таблица для LostItem <-> Tag
lostitem_tag = Table(
    "lostitem_tag",            # название ассоциативной таблицы
    Base.metadata,
    Column("lost_item_id", ForeignKey("lost_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


# Ассоциативная таблица для FoundItem <-> Tag
founditem_tag = Table(
    "founditem_tag",
    Base.metadata,
    Column("found_item_id", ForeignKey("found_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Связь только с LostItem (в будущем можно добавить и found_items)
    lost_items: Mapped[list["LostItem"]] = relationship(
        "LostItem",
        secondary=lostitem_tag,          # указываем таблицу связи
        back_populates="tags"            # ссылаемся на поле "tags" в LostItem
    )

    found_items: Mapped[list["LostItem"]] = relationship(
        "FoundItem",
        secondary=founditem_tag,
        back_populates="tags"
    )

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_items: Mapped[list["LostItem"]] = relationship(back_populates="category")
    found_items: Mapped[list["FoundItem"]] = relationship(back_populates='category')


class LostItem(Base):
    __tablename__ = "lost_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="lost_items")
    # Добавляем связь "tags":
    tags: Mapped[list["Tag"]] = relationship(
        secondary=lostitem_tag,   # та же таблица lostitem_tag
        back_populates="lost_items"
    )


class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates='found_items')
    # Добавляем связь "tags":
    tags: Mapped[list["Tag"]] = relationship(
        secondary=founditem_tag,   # та же таблица founditem_tag
        back_populates="found_items"
    )
