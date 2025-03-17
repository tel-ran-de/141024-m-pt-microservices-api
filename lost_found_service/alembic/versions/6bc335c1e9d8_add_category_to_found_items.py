"""add category to found items

Revision ID: 6bc335c1e9d8
Revises: c5c367980cbe
Create Date: 2025-03-12 13:56:48.412791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Импортируйте ваши модели:
from models import Category, LostItem, FoundItem


# revision identifiers, used by Alembic.
revision: str = '6bc335c1e9d8'
down_revision: Union[str, None] = 'c5c367980cbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # 1) Добавляем категории
    categories = [
        Category(name="Документы", description="Паспорта, удостоверения, пропуска"),
        Category(name="Техника", description="Смартфоны, ноутбуки, фотоаппараты"),
        Category(name="Одежда", description="Куртки, обувь, свитера, аксессуары"),
        Category(name="Украшения", description="Браслеты, часы, кольца, цепочки"),
        Category(name="Прочее", description="Остальные вещи, не попавшие в другие категории"),
    ]
    session.add_all(categories)
    session.commit()

    # Получаем реальные объекты категорий (с их ID) из БД
    cat_docs = session.query(Category).filter_by(name="Документы").one()
    cat_tech = session.query(Category).filter_by(name="Техника").one()
    cat_clothes = session.query(Category).filter_by(name="Одежда").one()
    cat_jewelry = session.query(Category).filter_by(name="Украшения").one()
    cat_other = session.query(Category).filter_by(name="Прочее").one()

    # 2) Добавляем потерянные вещи (LostItem)
    # При желании - разные даты, места, описания
    lost_items = [
        LostItem(
            name="Паспорт РФ на имя Иванова А.А.",
            description="Утерян возле метро Тверская, коричневая обложка",
            lost_date=datetime.now() - timedelta(days=5),
            location="Москва, м. Тверская",
            category_id=cat_docs.id,
        ),
        LostItem(
            name="Служебное удостоверение",
            description="Возможно выпало из сумки в автобусе №12",
            lost_date=datetime.now() - timedelta(days=3),
            location="Ростов-на-Дону, ул. Пушкина",
            category_id=cat_docs.id,
        ),
        LostItem(
            name="Смартфон Samsung Galaxy S21",
            description="Чёрный корпус, треснут экран, пропал в кафе",
            lost_date=datetime.now() - timedelta(days=10),
            location="Казань, ул. Баумана",
            category_id=cat_tech.id,
        ),
        LostItem(
            name="Ноутбук Lenovo",
            description="В синем рюкзаке вместе с зарядкой",
            lost_date=datetime.now() - timedelta(days=8),
            location="СПб, Невский проспект",
            category_id=cat_tech.id,
        ),
        LostItem(
            name="Куртка зелёная зимняя",
            description="На рукаве нашивка в виде снежинки",
            lost_date=datetime.now() - timedelta(days=1),
            location="Екатеринбург, ТЦ 'Гринвич'",
            category_id=cat_clothes.id,
        ),
        LostItem(
            name="Кепка Nike чёрная",
            description="Пропала после пробежки в парке",
            lost_date=datetime.now() - timedelta(days=2),
            location="Новосибирск, Центральный парк",
            category_id=cat_clothes.id,
        ),
        LostItem(
            name="Кроссовки Saucony беговые",
            description="Пропали из раздевалки спортзала",
            lost_date=datetime.now() - timedelta(days=7),
            location="Новосибирск, Центральный парк",
            category_id=cat_clothes.id,
        ),
        LostItem(
            name="Золотое кольцо с камнем",
            description="Подарок на помолвку, внутри гравировка",
            lost_date=datetime.now() - timedelta(days=12),
            location="Москва, парк Горького",
            category_id=cat_jewelry.id,
        ),
        LostItem(
            name="Платиновое кольцо с камнем",
            description="Подарок на помолвку, внутри гравировка",
            lost_date=datetime.now() - timedelta(days=15),
            location="Москва, парк Горького",
            category_id=cat_jewelry.id,
        ),
        LostItem(
            name="Серёжка с жемчугом",
            description="Одна штука, потеряна во время концерта",
            lost_date=datetime.now() - timedelta(days=7),
            location="СПб, Ледовый дворец",
            category_id=cat_jewelry.id,
        ),
        LostItem(
            name="Плюшевый мишка",
            description="Детская игрушка, голубого цвета",
            lost_date=datetime.now() - timedelta(days=4),
            location="Казань, парк Урицкого",
            category_id=cat_other.id,
        ),
        LostItem(
            name="Плетёная корзина",
            description="Осталась после пикника, кто-то забрал случайно",
            lost_date=datetime.now() - timedelta(days=15),
            location="Москва, парк Сокольники",
            category_id=cat_other.id,
        ),
    ]
    session.add_all(lost_items)
    session.commit()

    # 3) Добавляем найденные вещи (FoundItem)
    found_items = [
        FoundItem(
            name="Смартфон iPhone 12 в синем чехле",
            description="Найден на скамейке возле кофейни",
            found_date=datetime.now() - timedelta(days=2),
            location="Москва, ул. Арбат",
            category_id=cat_tech.id,
        ),
        FoundItem(
            name="Фотоаппарат Canon",
            description="Найден в такси (забыл пассажир)",
            found_date=datetime.now() - timedelta(days=1),
            location="СПб, Московский вокзал",
            category_id=cat_tech.id,
        ),
        FoundItem(
            name="Фотоаппарат Nikon",
            description="Найден в лесу",
            found_date=datetime.now() - timedelta(days=11),
            location="СПб, Московский вокзал",
            category_id=cat_tech.id,
        ),
        FoundItem(
            name="Зонт чёрный",
            description="Внутри забавный рисунок, кто-то оставил в гардеробе",
            found_date=datetime.now() - timedelta(days=6),
            location="Новосибирск, оперный театр",
            category_id=cat_clothes.id,
        ),
        FoundItem(
            name="Зонт розовый",
            description="Внутри забавный рисунок, кто-то оставил в туалете",
            found_date=datetime.now() - timedelta(days=2),
            location="Новосибирск, оперный театр",
            category_id=cat_clothes.id,
        ),
        FoundItem(
            name="Шарф вязаный, серый",
            description="Похоже, детский, оставлен в автобусе",
            found_date=datetime.now() - timedelta(days=3),
            location="Екатеринбург, маршрутка №18",
            category_id=cat_clothes.id,
        ),
        FoundItem(
            name="Шапка Custo, красная",
            description="Похоже, детская, оставлена в трамвая",
            found_date=datetime.now() - timedelta(days=3),
            location="Екатеринбург, маршрутка №18",
            category_id=cat_clothes.id,
        ),
        FoundItem(
            name="Серебряная цепочка",
            description="Без кулона, найдена на танцполе в клубе",
            found_date=datetime.now() - timedelta(days=1),
            location="Казань, ночной клуб 'Aurora'",
            category_id=cat_jewelry.id,
        ),
        FoundItem(
            name="Наручные часы (Casio)",
            description="Нашли в раздевалке спортивного зала",
            found_date=datetime.now() - timedelta(hours=12),
            location="Москва, фитнес-центр 'Energy'",
            category_id=cat_jewelry.id,
        ),
        FoundItem(
            name="Умные часы (Pebble)",
            description="Нашли в раздевалке бассейне",
            found_date=datetime.now() - timedelta(hours=13),
            location="Москва, фитнес-центр 'Energy'",
            category_id=cat_jewelry.id,
        ),
        FoundItem(
            name="Удостоверение личности",
            description="В кармане куртки, которую сдали в химчистку",
            found_date=datetime.now() - timedelta(days=5),
            location="СПб, химчистка 'Белый лотос'",
            category_id=cat_docs.id,
        ),
        FoundItem(
            name="Права категории B",
            description="Обнаружены на стойке информации",
            found_date=datetime.now() - timedelta(days=1),
            location="Ростов-на-Дону, ТЦ 'Мега'",
            category_id=cat_docs.id,
        ),
        FoundItem(
            name="Ключи от машины VW",
            description="На брелоке надпись 'Love my Golf'",
            found_date=datetime.now() - timedelta(days=2),
            location="Москва, парковка ТЦ 'Европейский'",
            category_id=cat_other.id,
        ),
        FoundItem(
            name="Ключи от машины Opel",
            description="На брелоке надпись 'Hate my rust car'",
            found_date=datetime.now() - timedelta(days=3),
            location="Москва, парковка ТЦ 'Европейский'",
            category_id=cat_other.id,
        ),
        FoundItem(
            name="Фитнес-браслет Mi Band",
            description="Обнаружен в раздевалке бассейна",
            found_date=datetime.now() - timedelta(days=4),
            location="СПб, бассейн 'Нептун'",
            category_id=cat_other.id,
        ),
    ]
    session.add_all(found_items)
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    # Удалим только те объекты, которые мы явно создавали, чтобы не снести реальные данные

    # Удаляем найденные вещи
    session.execute(sa.text("DELETE FROM found_items WHERE location IN "
        "('Москва, ул. Арбат','СПб, Московский вокзал','Новосибирск, оперный театр', "
        "'Екатеринбург, маршрутка №18','Казань, ночной клуб ''Aurora''','Москва, фитнес-центр ''Energy''', "
        "'СПб, химчистка ''Белый лотос''','Ростов-на-Дону, ТЦ ''Мега''','Москва, парковка ТЦ ''Европейский''','СПб, бассейн ''Нептун''')"
    ))
    # Удаляем потерянные вещи
    session.execute(sa.text("DELETE FROM lost_items WHERE location IN "
        "('Москва, м. Тверская','Ростов-на-Дону, ул. Пушкина','Казань, ул. Баумана','СПб, Невский проспект', "
        "'Екатеринбург, ТЦ ''Гринвич''','Новосибирск, Центральный парк','Москва, парк Горького','СПб, Ледовый дворец', "
        "'Казань, парк Урицкого','Москва, парк Сокольники')"
    ))
    # Удаляем категории, если хотим
    session.execute(sa.text("DELETE FROM categories WHERE name IN "
        "('Документы','Техника','Одежда','Украшения','Прочее')"
    ))
    session.commit()
