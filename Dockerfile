FROM tiangolo/uvicorn-gunicorn:python3.7

WORKDIR /app

COPY ./requirements/requeriments.txt .
COPY ./api/v1 ./api/v1/
COPY ./main.py .

RUN pip install -r requeriments.txt
