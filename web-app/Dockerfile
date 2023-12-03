FROM python:3.8-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


RUN git clone --depth 1 --branch main https://github.com/software-students-fall2023/4-containerized-app-exercise-goat.git /web-app

EXPOSE 3000


CMD ["python3", "app.py"]
