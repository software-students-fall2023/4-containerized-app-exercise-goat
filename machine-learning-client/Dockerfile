FROM python:3.8-slim

ENV GOOGLE_APPLICATION_CREDENTIALS="sunny-resolver-406200-d6e8c0dfe225.json"

WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app


EXPOSE 5000


CMD ["python3", "app.py"]
