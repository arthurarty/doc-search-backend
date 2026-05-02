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

## Running the application:
```bash
fastapi dev
```
