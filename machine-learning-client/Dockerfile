# Stage 1: Clone the repository and copy the desired folder
FROM python:3.8-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone --depth 1 --branch main https://github.com/software-students-fall2023/4-containerized-app-exercise-goat.git

# Stage 2: Copy only the necessary folder from the builder stage
FROM python:3.8-slim

ENV GOOGLE_APPLICATION_CREDENTIALS="sunny-resolver-406200-d6e8c0dfe225.json"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/4-containerized-app-exercise-goat/machine-learning-client /app

EXPOSE 3000

CMD ["python3", "app.py"]
