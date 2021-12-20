FROM tiangolo/uvicorn-gunicorn:python3.7

WORKDIR /code

COPY ./requeriments.txt /code/requeriments.txt
COPY ./setup.py /code/setup.py
COPY ./app /code/app

RUN pip install -r /code/requeriments.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]