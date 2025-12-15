FROM python:3.12-slim

# Install curl for compose health check
RUN apt-get update && apt-get install -y curl

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

ENV PYTHONPATH=/code

COPY ./app /code/backend/app

CMD ["python", "backend/app/main.py"]