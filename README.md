# Проект "Бюро находок"

## Запуск проекта

1. Создайте виртуальное окружение
2. Установите зависимости из файла requirements.txt
3. Создайте файл .env.local, используя .env.local.examples
4. Создайте DB, используя параметры из .env.local
5. Примените миграции
    ```bash
   alembic upgrade head 
    ```
6. Запустите сервер
   ```bash
   uvicorn main:app --reload
   ```

## Запуск автотестов

1. Создайте тестовую DB, используя параметры из .env.local
2. Запустите автотесты
   ```bash
   pytest -v
   ```


# History

## Урок 10

- добавили зависимости в `requirements.txt`
- создали `.gitignore`

**commit: `Урок 10: init`**

### 1. Основные файлы и конфигурация

- **`main.py`**:
  - Этот файл является точкой входа в ваше FastAPI приложение.
  - Он инициализирует приложение FastAPI и подключает маршрутизаторы (`routers`) для обработки запросов, связанных с потерянными и найденными предметами.
  - Содержит базовый эндпоинт `/`, который возвращает приветственное сообщение.

- **`config.py`**:
  - Содержит настройки приложения, такие как параметры подключения к базе данных.
  - Использует Pydantic для валидации и загрузки переменных окружения из файла `.env.local`.

- **`.env.local.example`**:
  - Пример файла переменных окружения, который используется для настройки параметров базы данных и других конфигураций.
  - Пользователи должны создать файл `.env.local` на основе этого примера и заполнить его своими данными.

### 2. База данных и модели

- **`database.py`**:
  - Настраивает подключение к базе данных с использованием SQLAlchemy.
  - Создает асинхронный движок и сессию для взаимодействия с базой данных.

- **`models.py`**:
  - Определяет модели данных для таблиц `lost_items` и `found_items`.
  - Использует SQLAlchemy ORM для определения структуры таблиц и их полей.
  - Каждая модель соответствует таблице в базе данных и определяет поля, такие как `id`, `name`, `description`, `date`, и `location`.

### 3. Маршрутизаторы и эндпоинты

- **`routers/lost_items.py` и `routers/found_items.py`**:
  - Определяют маршрутизаторы для обработки HTTP-запросов, связанных с потерянными и найденными предметами.
  - Каждый маршрутизатор содержит CRUD (Create, Read, Update, Delete) операции для соответствующих моделей.
  - Используют Pydantic схемы для валидации входных данных и сериализации ответов.

### 4. Схемы данных

- **`schemas.py`**:
  - Определяет Pydantic схемы для валидации данных, поступающих в API, и для сериализации данных, возвращаемых из API.
  - Содержит схемы для создания, обновления и чтения потерянных и найденных предметов.

### 5. Тестирование

- **`conftest.py`**:
  - Содержит фикстуры для настройки тестовой базы данных и клиента FastAPI.
  - Использует `pytest` и `pytest-asyncio` для асинхронного тестирования.
  - Фикстуры обеспечивают изоляцию тестов, создавая и уничтожая тестовую базу данных перед и после выполнения тестов.

- **`test_found_items.py` и `test_lost_items.py`**:
  - Содержат тесты для проверки функциональности эндпоинтов, связанных с найденными и потерянными предметами.
  - Включают тесты для создания, чтения, обновления и удаления предметов, а также проверки на корректность обработки ошибок (например, когда предмет не найден).

### 6. Миграции базы данных

- **`alembic.ini` и `alembic/env.py`**:
  - Конфигурационные файлы для Alembic, инструмента для управления миграциями базы данных.
  - `alembic.ini` содержит основные настройки, такие как путь к скриптам миграций.
  - `env.py` настраивает окружение для выполнения миграций, подключаясь к базе данных и используя метаданные моделей.

- **`789953bf9c87_init_migrations.py`**:
  - Автоматически сгенерированная миграция, которая создает таблицы `found_items` и `lost_items` в базе данных.
  - Содержит команды для создания и удаления таблиц и индексов.

**commit: `Урок 10: создан простой FastAPI проект`**


## Урок 11

1. **Обновление README.md:**
   - Добавлен новый раздел "Урок 11", который описывает команды для создания и применения миграции, добавляющей категории к потерянным предметам.
   - Указаны команды `alembic revision --autogenerate -m "add category to lost items"` и `alembic upgrade head` для генерации и применения миграции.

2. **Изменения в models.py:**
   - Добавлена новая модель `Category`, представляющая категории, к которым могут относиться потерянные предметы.
   - В модель `LostItem` добавлены поля `category_id` и `category`, которые устанавливают связь с моделью `Category`.
   - Используется `relationship` для установки двусторонней связи между `LostItem` и `Category`.

3. **Изменения в routers/lost_items.py:**
   - В маршруте создания потерянного предмета добавлена проверка существования категории по `category_id`.
   - Если категория не найдена, возвращается ошибка `404 Not Found`.

4. **Изменения в schemas.py:**
   - В схему `LostItemBase` добавлено поле `category_id` для валидации данных, связанных с категорией.
   - Добавлены новые схемы `CategoryCreate`, `CategoryUpdate`, и `CategoryRead` для работы с категориями.
   - Эти схемы позволяют создавать, обновлять и читать данные категорий, обеспечивая валидацию и сериализацию.

**Зачем нужны эти изменения:**

- Введение категорий позволяет лучше структурировать данные о потерянных предметах, упрощая их фильтрацию и организацию.
- Проверка существования категории при создании предмета предотвращает ошибки, связанные с несуществующими категориями.
- Новые схемы для категорий обеспечивают согласованность и валидацию данных на уровне API.

- создание файла миграции:
`alembic revision --autogenerate -m "add category to lost items"`
- после этого нужно внести изменения в новый файл миграций в разделах `upgrade` и `downgrade` для того чтобы можно было накатить миграции на непустую базу.
- после внесения изменений в файл миграции, применить миграцию:
`alembic upgrade head`

**commit: `Урок 11: добавлены категории к потерянным предметам`**

1. **Изменения в models.py:**
   - В модель `Category` добавлено поле `found_items`, которое устанавливает связь с моделью `FoundItem`.
   - В модель `FoundItem` добавлены поля `category_id` и `category`, которые устанавливают связь с моделью `Category`.
   - Используется `relationship` для установки двусторонней связи между `FoundItem` и `Category`.

**Зачем нужны эти изменения:**

- Введение категорий для найденных предметов позволяет лучше структурировать данные, упрощая их фильтрацию и организацию.
- Связь между `FoundItem` и `Category` обеспечивает согласованность данных и позволяет легко определять, к какой категории относится найденный предмет.
- Обновление README.md помогает пользователям понять, как создавать и применять миграции, а также учитывать особенности работы с непустой базой данных.

- создание файла миграции:
`alembic revision --autogenerate -m "add category to found items"`
- после этого нужно внести изменения в новый файл миграций в разделах `upgrade` и `downgrade` для того чтобы можно было накатить миграции на непустую базу.
- после внесения изменений в файл миграции, применить миграцию:
`alembic upgrade head`

**commit: `Урок 11 (ПРАКТИКА): добавлены категории к найденным предметам`**

1. **Обновление main.py:**
   - Добавлен новый маршрутизатор `categories_router` для обработки запросов, связанных с категориями.
   - Подключен маршрутизатор к основному приложению FastAPI с префиксом `/categories` и тегом `["categories"]`.

2. **Изменения в routers/found_items.py:**
   - В маршруте создания найденного предмета добавлена проверка существования категории по `category_id`.
   - Если категория не найдена, возвращается ошибка `404 Not Found`.

3. **Изменения в schemas.py:**
   - В схему `FoundItemBase` добавлено поле `category_id` для валидации данных, связанных с категорией.
   - Это позволяет убедиться, что при создании найденного предмета указывается существующая категория.

**Зачем нужны эти изменения:**

- Введение маршрутизатора для категорий позволяет управлять категориями через API, добавляя, обновляя и удаляя их.
- Проверка существования категории при создании найденного предмета предотвращает ошибки, связанные с несуществующими категориями.
- Обновление схемы для найденных предметов обеспечивает согласованность и валидацию данных на уровне API.

**commit: `Урок 11 (ПРАКТИКА): добавлены маршрутизаторы для категорий и связаны найденные предметы с категориями`**

**commit: `Урок 11 (FIX): хотфикс, настройки подключения к БД`**


## Урок 12

### добавляем данные в БД для будущих экспериментов

- создание файла миграции:
`alembic revision --autogenerate -m "add category to found items"`
- после этого нужно внести изменения в новый файл миграций в разделах `upgrade` и `downgrade` для того чтобы можно было накатить миграции на непустую базу.
- после внесения изменений в файл миграции, применить миграцию:
`alembic upgrade head`

**commit: `Урок 12: добавлены данные в БД`**

### Пагинация, сортировка, фильтрация

#### Краткие пояснения

1. **`session = AsyncSessionLocal()`**  
   Создаём асинхронную сессию, чтобы иметь доступ к базе данных через SQLAlchemy.
2. **`await session.execute(query)`**  
   Выполняем асинхронный SQL-запрос (т.к. находимся внутри `async def main():`). Если бы это был чисто синхронный контекст, обернули бы в `asyncio.run(...)`. Но здесь у нас всё в `async def`.
3. **`select(...)`** — построение SQL-запроса.  
   - `.offset(N).limit(M)` — пагинация (пропускаем N, берём M).  
   - `.where(условие)` — фильтрация.  
   - `.order_by(...)` — сортировка.
4. **`.scalars().all()`**  
   Преобразует результат (курсор) в обычный Python-список объектов (LostItem / FoundItem).
5. **`print(...)`**  
   Выводим на экран результаты, чтобы убедиться, что запрос возвращает нужные записи.

#### Как запустить

1. Сохраните этот код в файл, например `test_db.py`.  
2. В терминале/консоли выполните:
   ```bash
   python test_db.py
   ```
3. Скрипт последовательно покажет:
   - **Пагинацию** (две «страницы»).
   - **Фильтрацию** (три разных условия).
   - **Сортировку** (три разных способа).

При таком подходе весь код выполняется внутри **одного** `asyncio.run(...)`, и не возникает проблем с «Event loop is closed».

**commit: `Урок 12: примеры для консоли`**

**commit: `Урок 12 (ПРАКТИКА): пагинация, фильтрация, сортировка`**

**commit: `Урок 12 (РЕШЕНИЕ): пагинация, фильтрация, сортировка`**

Ниже пример, **как внедрить пагинацию, фильтрацию и сортировку** непосредственно в роутер `lost_items.py`. Мы добавляем в эндпоинт `GET /lost_items/` несколько query-параметров:

- **`skip`** (int) — сколько записей пропустить (для пагинации).
- **`limit`** (int) — сколько записей вернуть (для пагинации).
- **`category_id`** (Optional[int]) — фильтрация по категории.
- **`location`** (Optional[str]) — фильтрация по содержанию текста в поле `location`.
- **`order_by`** (Optional[str]) — имя поля, по которому сортировать (например `"lost_date"` или `"name"`).
- **`sort_desc`** (bool) — сортировка по убыванию, если `True`; по умолчанию `False` (возрастание).

Таким образом, один эндпоинт покрывает все три задачи: **пагинация**, **фильтрация** и **сортировка**.

### Как это работает

1. **Query-параметры**:
   - `skip` и `limit` (пагинация): пропускаем `skip` записей и берём `limit`.
   - `category_id` и `location` (фильтрация): если пользователь указал — добавляем `WHERE category_id = ...` или `WHERE location ILIKE '%...%'`.
   - `order_by` и `sort_desc` (сортировка): собираем `ORDER BY` по нужному полю, и если `sort_desc=True`, делаем убывающий порядок (`desc()`).
   
2. **`ilike(...)`**  
   Делаем регистронезависимый поиск по локации. Это удобно для поиска текста, например `"МосКвА"` будет найдено, если в БД есть `"Москва"`.
   
3. **Проверка поля сортировки**  
   - Если в `order_by` пользователь передал строку, например `"lost_date"`, через `getattr(models.LostItem, order_by, None)` мы пытаемся получить атрибут модели. Если его нет, пропускаем сортировку.
   - Если атрибут есть, добавляем `.order_by(column_attr.desc())` или `.order_by(column_attr.asc())`.

4. **Документация в Swagger**  
   - `Query(...)` с параметрами `description=...` сделает так, что в `/docs` (Swagger) эти параметры будут подробно отражены.

Теперь эндпоинт `GET /lost_items/` можно вызвать, например, так:
```
GET /lost_items/?skip=5&limit=5&category_id=2&location=москва&order_by=lost_date&sort_desc=true
```
и вы получите *следующие* 5 записей (пропущено 5), из категории id=2, у которых в локации есть `москва` (регистронезависимо), отсортированные по `lost_date` убыванию.

**commit: `Урок 12: пагинация, фильтрация, сортировка в lost_items`**

**commit: `Урок 12 (ПРАКТИКА): пагинация, фильтрация, сортировка в found_items`**

Ниже — пример обновлённого `routers/found_items.py`, в котором добавлены такие же механизмы **пагинации**, **фильтрации** и **сортировки**, как и для `lost_items`. Мы используем следующие query-параметры:

- **`skip`** (int, по умолчанию 0) — сколько записей пропустить.
- **`limit`** (int, по умолчанию 10) — сколько записей вернуть.
- **`category_id`** (Optional[int]) — если указано, фильтруем только найденные вещи в нужной категории.
- **`location`** (Optional[str]) — если указано, ищем по содержанию текста в поле `location` (через ilike).
- **`order_by`** (Optional[str]) — имя поля, по которому сортируем (например `"found_date"`, `"name"`).
- **`sort_desc`** (bool) — если `True`, сортируем по убыванию; по умолчанию `False` (по возрастанию).

Все эти параметры **необязательны** (Optional), и благодаря этому один эндпоинт может охватить все сценарии: **пагинация**, **фильтрация** и/или **сортировка**.

### Объяснения по коду

1. **Query-параметры**:
   - `skip` (пагинация): сколько строк пропустить (по умолчанию 0).  
   - `limit` (пагинация): сколько строк вернуть (по умолчанию 10).  
   - `category_id` (фильтрация): если задано, добавляем `WHERE category_id = ...`.  
   - `location` (фильтрация): если задано, добавляем `WHERE location ILIKE '%...%'`.  
   - `order_by` (сортировка): имя столбца (например, `"found_date"`).  
   - `sort_desc` (bool): `True` — убывание, `False` — возрастание.

2. **Логика запроса**:
   1. Начинаем с `query = select(models.FoundItem)`.
   2. Применяем `WHERE`-условия, если пользователь передал фильтрационные параметры.
   3. Если пользователь указал `order_by`, получаем атрибут у модели (`getattr(models.FoundItem, order_by)`) и устанавливаем `order_by(... .desc())` или `order_by(... .asc())`.
   4. Применяем `.offset(skip).limit(limit)` для пагинации.
   5. Выполняем запрос (`await db.execute(query)`) и скаляризуем в Python-список (`.scalars().all()`).

3. **Документация в Swagger**:
   - Благодаря `Query(...)` с `description` всё будет видимо в `/docs`.

4. **Примеры вызова**:
   - `/found_items/?limit=5&order_by=found_date&sort_desc=true`  
     Получаем 5 последних найденных (самые свежие вверху).  
   - `/found_items/?skip=10&limit=5&category_id=2&location=Арбат`  
     Пропускаем первые 10, затем берём 5 записей только из категории id=2, у которых в `location` есть «Арбат» (регистронезависимо).

Таким образом, ваш эндпоинт для **found_items** теперь аналогично поддерживает пагинацию, фильтрацию и сортировку.

**commit: `Урок 12 (РЕШЕНИЕ): пагинация, фильтрация, сортировка в found_items`**


## Урок 13

**Описание изменений:**

- **Изменения в models.py:**
  - Добавлена ассоциативная таблица `lostitem_tag` для связи между `LostItem` и `Tag`.
  - Создана новая модель `Tag`, представляющая теги, которые могут быть привязаны к потерянным предметам.
  - В модель `Tag` добавлено поле `lost_items`, которое устанавливает связь с моделью `LostItem` через ассоциативную таблицу `lostitem_tag`.
  - В модель `LostItem` будет добавлено поле `tags` для обратной связи с тегами (необходимо будет внести изменения в `LostItem` для завершения этой связи).

**Зачем нужны эти изменения:**

- Введение тегов позволяет более гибко классифицировать потерянные предметы, добавляя возможность привязывать несколько тегов к одному предмету.
- Это улучшает фильтрацию и поиск потерянных предметов, делая систему более удобной для пользователей.
- Ассоциативная таблица `lostitem_tag` обеспечивает правильную организацию связей "многие ко многим" между потерянными предметами и тегами.

- создание файла миграции:
`alembic revision --autogenerate -m "add Tag table and lostitem_tag association"`
- применение миграции:
`alembic upgrade head`

**commit: `Урок 13: добавление тегов для потерянных предметов`**

1. **Изменения в routers/lost_items.py:**
   - Добавлен импорт `selectinload` из `sqlalchemy.orm` для загрузки связанных данных.
   - В маршруте `read_lost_items` добавлена опция `selectinload` для загрузки связанных тегов (`tags`) вместе с потерянными предметами.
   - Это позволяет загружать теги в один запрос, улучшая производительность при чтении данных.

2. **Изменения в schemas.py:**
   - Добавлены новые схемы для работы с тегами: `TagBase`, `TagCreate`, `TagUpdate`, и `TagRead`.
   - В схему `LostItem` добавлено поле `tags`, которое возвращает список тегов, связанных с потерянным предметом.
   - Эти изменения обеспечивают валидацию и сериализацию данных тегов, а также их возврат при запросах на получение потерянных предметов.

**Зачем нужны эти изменения:**

- Введение тегов для потерянных предметов позволяет более гибко классифицировать предметы, добавляя возможность привязывать несколько тегов к одному предмету.
- Использование `selectinload` улучшает производительность при загрузке связанных данных, уменьшая количество запросов к базе данных.
- Новые схемы для тегов обеспечивают согласованность и валидацию данных на уровне API.

**Дополнительная информация:**

- По умолчанию SQLAlchemy делает «ленивую» загрузку M:N связей (lazy load). При сериализации ответа `LostItem` может не подтянуться список `tags` (или подтянется в отдельном запросе только при обращении к `item.tags`, что в асинхронном контексте FastAPI может вернуть пустой список, если не вызвать вручную).
- `selectinload` или `joinedload` заставляют SQLAlchemy «жадно» (eager) загрузить связанные объекты:
  - `selectinload` сделает несколько запросов по принципу `SELECT ... WHERE lost_item_id IN (...)`.
  - `joinedload` сделает один большой `JOIN` (если нужно вернуть теги в одном запросе).
- Схема `LostItem` содержит поле `tags: list[TagRead]`, поэтому, когда вы возвращаете `items`, Pydantic умеет подтянуть и сериализовать эти теги в JSON.

**commit: `Урок 13: обновление схем и эндпоинта read_lost_items`**

1. **Добавлен новый маршрутизатор `routers/tags.py`:**
   - Реализованы CRUD-операции для тегов:
     - `POST /tags` — создание нового тега (с проверкой на уникальность).
     - `GET /tags` — получение списка всех тегов.
     - `GET /tags/{tag_id}` — получение конкретного тега по ID.
     - `PUT /tags/{tag_id}` — обновление имени тега (с проверкой на дублирование).
     - `DELETE /tags/{tag_id}` — удаление тега.
   - Эти маршруты позволяют управлять тегами независимо от их использования в `LostItem` или `FoundItem`.

2. **Обновления в `main.py`:**
   - Подключён новый роутер `tags_router` с префиксом `/tags`.
   - Теперь API поддерживает работу с тегами на отдельном эндпоинте.

3. **Изменения в `schemas.py`:**
   - Добавлены новые схемы:
     - `TagBase` — базовая схема для тегов.
     - `TagCreate` — схема для создания тегов.
     - `TagRead` — схема для возврата данных о теге.
   - Эти схемы обеспечивают валидацию и сериализацию данных тегов.

**Зачем нужны эти изменения:**
- Позволяют управлять тегами отдельно от объектов `LostItem` и `FoundItem`.
- Добавляют API-интерфейс для создания, редактирования и удаления тегов.
- Гарантируют, что теги имеют уникальные имена, исключая дублирование.
- Обеспечивают правильную сериализацию данных тегов при их возврате.

**Дополнительная информация:**
- Валидация `TagCreate` гарантирует, что тег нельзя создать, если он уже есть в базе.
- При обновлении имени тега API проверяет, чтобы новое имя не совпадало с уже существующими тегами.
- SQLAlchemy автоматически удаляет привязки тегов в `lostitem_tag` при удалении самого тега.

**commit: `Урок 13: добавление CRUD-эндпоинтов для тегов`**


1. **Изменение в маршрутах привязки тегов (`attach_tag_to_lost_item`)**  
   - Вместо `db.get(...)` используем `select(...).options(selectinload(...))` для явной загрузки списка тегов.  
   - Устранили ошибку `MissingGreenlet`, возникавшую при ленивой загрузке (`lazy load`) в асинхронном режиме.

2. **Изменение в маршрутах отвязки тегов (`detach_tag_from_lost_item`)**  
   - Аналогично используем `selectinload(LostItem.tags)` перед проверкой `if tag in lost_item.tags:`.  
   - Это позволяет избежать повторного ленивого запроса к базе, который приводил к конфликту event loop и ошибке `MissingGreenlet`.

**Зачем нужны эти изменения:**
- В асинхронном режиме SQLAlchemy «лениво» подгружает связанные данные при первом обращении к `lost_item.tags`. Это иногда выпадает из event loop и вызывает `MissingGreenlet`.
- Использование `selectinload` заранее загружает теги одним дополнительным запросом в момент получения LostItem, так что при проверке `if tag in lost_item.tags:` не происходит повторного запроса «вручную».
- В результате, привязка и отвязка тегов в асинхронном FastAPI теперь работает корректно и не выбрасывает исключений, связанных с «зелёными нитями» (greenlets).

**Дополнительная информация:**
- В асинхронном FastAPI стоит избегать «ленивой» загрузки M:N (lazy load), которая внутри может вызывать I/O вне нужного greenlet.  
- `selectinload(LostItem.tags)` или `joinedload(LostItem.tags)` решает проблему, обеспечивая «жадную» загрузку данных до обращения к полю `.tags`.
- Если в будущем понадобится аналогичная логика для FoundItem, следует применять тот же подход.  

**commit: `Урок 13: привязка/отвязка тегов (selectinload) для LostItem`**

**Зачем нужны эти изменения:**
- Готовим Many-to-Many связь FoundItem <-> Tag.
- Позволяет хранить, какие теги привязаны к найденным предметам.

**Доп. информация:**
- Это аналогично lostitem_tag, но теперь для FoundItem.

- создание файла миграции:
`alembic revision --autogenerate -m "add Tag table and founditem_tag association"`
- применение миграции:
`alembic upgrade head`

**commit: `Урок 13 (РЕШЕНИЕ): добавление тегов для найденных предметов`**

**Зачем нужны эти изменения:**
- Пользователи теперь могут создавать/получать/редактировать объекты FoundItem, 
  и видеть/редактировать список тегов (в будущем шаге).

**Доп. информация:**
- Если CRUD для FoundItem уже был, мы просто дорабатываем схему и добавляем selectinload для тегов.

**commit: `Урок 13 (РЕШЕНИЕ): обновление схем и эндпоинта для найденных предметов`**

**Зачем нужны эти изменения:**
- Дают пользователям возможность динамически привязывать и отвязывать теги у FoundItem.
- Завершают реализацию Many-to-Many для FoundItem.

**Доп. информация:**
- Избегаем MissingGreenlet, так как мы не полагаемся на ленивую загрузку 
  при обращении found_item.tags.
- Теперь FoundItem полностью аналогичен LostItem по работе с тегами.

**commit: `Урок 13 (РЕШЕНИЕ): привязка/отвязка тегов (selectinload) для FoundItem`**