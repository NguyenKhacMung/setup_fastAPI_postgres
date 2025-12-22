# FastAPI Production Boilerplate 2025

## Table of Contents
- [Installation](#installation)
- [Running the app](#run-app)
- [Migration database](#migration-database)

## Installation
1. Clone the source code to your computer.

2. Create and activate virtualenv: 
```bash 
python -m venv venv 
venv\Scripts\activate # Windows 
# or 
source venv/bin/activate # Mac/Linux 
```
3. Install library: 
```bash 
pip install -r requirements.txt 
```

## Run app
```bash
python -m app.main 
--
uvicorn app.main:app --reload

```
App runs at http://localhost:8000/docs

## Database Migration with Alembic 
alembic init alembic

1. Create a new migration:
```bash
alembic revision --autogenerate -m "initial"

```
2. Run the migrate/update database:

```bash
alembic upgrade head

```
2. Run the revert database:

```bash
alembic downgrade -1
```
> **Note**: Edit the connection and DB name in `.env` and `alembic.ini` if necessary.
