FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get -y install sqlite3

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/app.py"]