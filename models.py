from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


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


class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates='found_items')