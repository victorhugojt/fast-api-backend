FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./setup.py /code/setup.py
COPY ./app /code/app

RUN pip install -r /code/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# CMD ["opentelemetry-instrument", "--traces_exporter", "otlp,console", "--metrics_exporter", "none", "--service_name", "greeting-service", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]