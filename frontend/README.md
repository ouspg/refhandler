# fastapi-test

Simple test for running FastAPI-based Python applications using Docker compose.

## How to deploy

1. Run the command `docker-compose up` in the main folder
2. Open <http://localhost:8000/> in your browser

## How to rebuild

If you made any changes to the code, rebuild your local docker image using 

- `docker-compose build` just to rebuild
- `docker-compose up --build` to rebuild and deploy
