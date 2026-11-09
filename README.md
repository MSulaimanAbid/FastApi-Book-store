# FastAPI Book Store

A simple RESTful API for managing a bookstore, built with **FastAPI** and backed by a **PostgreSQL** database hosted on [Neon](https://neon.tech).

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ASGI Server | [Uvicorn](https://www.uvicorn.org/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| DB Driver | [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) |
| Validation | [Pydantic](https://docs.pydantic.dev/) |
| Env Management | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Database | PostgreSQL (Neon — serverless cloud Postgres) |

---

## Project Structure

```
FastApi-Book-store/
├── main.py          # FastAPI app + all route handlers (HTTP layer)
├── services.py      # CRUD functions — all database logic lives here
├── models.py        # SQLAlchemy ORM model → maps to the "books" table
├── schemas.py       # Pydantic schemas for request validation & responses
├── db.py            # DB engine, session factory, Base, and get_db dependency
├── requirements.txt # Python dependencies
├── .env             # Secret environment variables (git-ignored)
└── .env.example     # Template showing required environment variables
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/books` | Get all books |
| `GET` | `/books/{id}` | Get a single book by id |
| `POST` | `/books` | Create a new book |
| `PUT` | `/books/{id}` | Update an existing book by id |
| `DELETE` | `/books/{id}` | Delete a book by id |

All endpoints return a `Book` object (or list of `Book` objects) with the following shape:

```json
{
  "id": 1,
  "title": "The Pragmatic Programmer",
  "description": "A guide to software craftsmanship",
  "author": "David Thomas",
  "year": 1999
}
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/FastApi-Book-store.git
cd FastApi-Book-store
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your database URL:

```bash
cp .env.example .env
```

Inside `.env`:

```env
SQL_URL=postgresql://user:password@host/dbname?sslmode=require
```

> The app uses a Neon PostgreSQL instance. You can get a free connection string from [neon.tech](https://neon.tech).

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## Interactive Docs

FastAPI generates documentation automatically:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI — interactive API explorer |
| `http://127.0.0.1:8000/redoc` | ReDoc — clean API reference |

---

## How It Works

```
Request → main.py (route handler)
              ↓
         services.py (DB logic)
              ↓
         models.py (ORM / table)
              ↓
         PostgreSQL (Neon)
              ↓
         schemas.py (serialize response)
              ↓
Response
```

1. **`main.py`** — Receives the HTTP request, validates it via Pydantic schemas, and delegates to `services.py`.
2. **`services.py`** — Runs the actual SQLAlchemy queries (create, read, update, delete).
3. **`models.py`** — Defines the `Book` ORM model that maps to the `books` table.
4. **`schemas.py`** — Defines Pydantic schemas used to validate incoming data and serialize outgoing responses.
5. **`db.py`** — Sets up the SQLAlchemy engine and session, and provides the `get_db` dependency injected into every route.

---

## Requirements

```
fastapi
uvicorn
SQLAlchemy
pydantic
psycopg2-binary
python-dotenv
```

Install all with:

```bash
pip install -r requirements.txt
```
# FastAPI Book Store

A simple RESTful API for managing a bookstore, built with **FastAPI** and backed by a **PostgreSQL** database hosted on [Neon](https://neon.tech).

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ASGI Server | [Uvicorn](https://www.uvicorn.org/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| DB Driver | [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) |
| Validation | [Pydantic](https://docs.pydantic.dev/) |
| Env Management | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Database | PostgreSQL (Neon — serverless cloud Postgres) |

---

## Project Structure

```
FastApi-Book-store/
├── main.py          # FastAPI app + all route handlers (HTTP layer)
├── services.py      # CRUD functions — all database logic lives here
├── models.py        # SQLAlchemy ORM model → maps to the "books" table
├── schemas.py       # Pydantic schemas for request validation & responses
├── db.py            # DB engine, session factory, Base, and get_db dependency
├── requirements.txt # Python dependencies
├── .env             # Secret environment variables (git-ignored)
└── .env.example     # Template showing required environment variables
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/books` | Get all books |
| `GET` | `/books/{id}` | Get a single book by id |
| `POST` | `/books` | Create a new book |
| `PUT` | `/books/{id}` | Update an existing book by id |
| `DELETE` | `/books/{id}` | Delete a book by id |

All endpoints return a `Book` object (or list of `Book` objects) with the following shape:

```json
{
  "id": 1,
  "title": "The Pragmatic Programmer",
  "description": "A guide to software craftsmanship",
  "author": "David Thomas",
  "year": 1999
}
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/FastApi-Book-store.git
cd FastApi-Book-store
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your database URL:

```bash
cp .env.example .env
```

Inside `.env`:

```env
SQL_URL=postgresql://user:password@host/dbname?sslmode=require
```

> The app uses a Neon PostgreSQL instance. You can get a free connection string from [neon.tech](https://neon.tech).

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## Interactive Docs

FastAPI generates documentation automatically:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI — interactive API explorer |
| `http://127.0.0.1:8000/redoc` | ReDoc — clean API reference |

---

## How It Works

```
Request → main.py (route handler)
              ↓
         services.py (DB logic)
              ↓
         models.py (ORM / table)
              ↓
         PostgreSQL (Neon)
              ↓
         schemas.py (serialize response)
              ↓
Response
```

1. **`main.py`** — Receives the HTTP request, validates it via Pydantic schemas, and delegates to `services.py`.
2. **`services.py`** — Runs the actual SQLAlchemy queries (create, read, update, delete).
3. **`models.py`** — Defines the `Book` ORM model that maps to the `books` table.
4. **`schemas.py`** — Defines Pydantic schemas used to validate incoming data and serialize outgoing responses.
5. **`db.py`** — Sets up the SQLAlchemy engine and session, and provides the `get_db` dependency injected into every route.

---

## Requirements

```
fastapi
uvicorn
SQLAlchemy
pydantic
psycopg2-binary
python-dotenv
```

Install all with:

```bash
pip install -r requirements.txt
```
