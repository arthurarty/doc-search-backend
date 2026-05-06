# doc-search-backend
A restful API that powers a RAG application.

## Architecture
This project follows a `Service Orchestrator` design. Services house the business logic and use clients and other services to fulfil the requests.  
Any endpoint exposed by the API points to service. Any clients or services required by the service are passed to it using `Dependency injection`.  
The application is built to be stateless so that it can scale horizontally.   

## Document indexing
1. Document indexing starts with file upload. To upload a file the client requests for a signed url using the endpoint `/docs/signed-url/`.
1. Client then uploads the document to bucket using the signed url generated and updates the document status once the upload is complete with a request to the endpoint `/docs/{unique_identifier}`.
1. Updating the document status triggers indexing which happens as a background task run by `Celery`. The document is read from storage in chunks and embeddings created and stored in a vector store.

## Tech Stack
1. Postgres - serves the database and vector store.
1. Python FastAPI - Python framework for building restful api.
1. Ollama - To run models locally.
1. Celery - Task queue
1. Redis - message broker for task queue.
1. Google cloud storage - Object storage where documents are stored.

## Implemented features
1. File upload using pre-signed urls
1. Document chunking and indexing
1. Semantic search

## Pending tasks/features
1. Reranking semantic search results
1. AI Agent to answer questions with semantic search as a tool.
1. Document summarizing using LLM.
1. Unit tests using pytest.
1. CI pipeline using github actions.

# Development
## Requirements:
1. Python 3.14+
1. Virtualenv
1. [Docker](https://www.docker.com/)
1. [Ollama](https://ollama.com/)

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


## Running the application:  
To run the application you can use docker like this.
```bash
docker compose up
```
Once the application is running you can run migrations by accessing the app container.
```bash
docker compose exec app bash
```
Then to run the migration you can use the command.
```bash
alembic upgrade head
```
You can view the docs of the api using any browser and visiting the url `http://localhost:8000/docs`


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