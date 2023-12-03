# Stage 1: Clone the repository and copy the desired folder
FROM python:3.8-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone --depth 1 --branch main https://github.com/software-students-fall2023/4-containerized-app-exercise-goat.git

# Stage 2: Copy only the necessary folder from the builder stage
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/4-containerized-app-exercise-goat/web-app /app

EXPOSE 4000

CMD ["python3", "app.py"]



