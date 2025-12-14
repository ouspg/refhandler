FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/src

COPY ./app /src/backend/app

CMD ["python", "/src/backend/app/main.py"]