FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
EXPOSE 8002
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8002"]
