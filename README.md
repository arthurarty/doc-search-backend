# doc-search-backend
A backend built in FastAPI to power a document search.

## Requirements:
1. Python 3.14+
1. Virtualenv
1. Docker

## Setup process
Create a virtual environment and install the requirements.  
You can do that like this to create a virtual environment folder called `venv`
```bash
python -m venv venv
```
Activate the virtual environment like this
```bash
source venv/bin/activate
```
Install requirements
```bash
pip install -r requirements.txt
```
Install pre-commit
```bash
pre-commit install
```
Build the docker container, this will run a Postgres Database that has PGVector installed.
```bash
docker compose up
```

## Migrations
The app uses Alembic to manage database migrations.  
To create a new migration run the command.
```bash
alembic revision --autogenerate -m "<message>"
```
To see the current revision you can use the command.
```bash
alembic current
```
To upgrade(to run a new migration)
```bash
alembic upgrade head
```
To roll back the last migration you can use the command.
```bash
alembic downgrade -1
```

## Running the application:
You need to have the docker container running in the background or another terminal.  
You should have run migrations before trying to run the application.
```bash
fastapi dev
```
