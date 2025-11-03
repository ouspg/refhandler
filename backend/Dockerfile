FROM python:3.12-slim

WORKDIR /app

#RUN apt-get update && apt-get -y install sqlite3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY ./app /app/app

CMD ["python", "app/main.py"]