import logging
import random
import time
import os
from typing import Optional
from app.instrumentation import metrics_exporter
from fastapi import Response, APIRouter
from opentelemetry import trace, baggage
from opentelemetry.context import attach, detach


metrics = metrics_exporter.config('greetings-service')
meter = metrics.get_meter(__name__)

router = APIRouter()
tracer = trace.get_tracer(__name__)
http_requests_counter = meter.create_counter("http_requests_counter")
http_rt = meter.create_histogram("http_rt")



@router.get("/")
async def read_root():
    logging.error("Hello World")
    return {"Hello": "World"}


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logging.error("items")
    return {"item_id": item_id, "q": q}


@router.get("/io_task")
async def io_task():
    time.sleep(1)
    logging.error("io task")
    return "IO bound task finish!"


@router.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
    logging.error("cpu task")
    return "CPU bound task finish!"


@router.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    logging.error("random status")
    return {"path": "/random_status"}


@router.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random sleep")
    return {"path": "/random_sleep"}


@router.get("/error_test")
async def error_test(response: Response):
    logging.error("got error!!!!")
    raise ValueError("value error")


def another_thing_to_do():
    return "have a good weekend"


@router.get("/hi", status_code=200)
async def greeting():
    user = attach(
        baggage.set_baggage("user.id", "Pibe Valderrama")
    )
    with tracer.start_as_current_span("Greeting Request", attributes={ "requires env": "HOME", "library":"FastAPI" } ):
        parent_context = baggage.set_baggage("position", "10")
        name = os.environ['NAME']
        with tracer.start_as_current_span("Child Span", context=parent_context):
            child_context = baggage.set_baggage("matches", "467")
            message = "Hello {} !. {}".format(name, another_thing_to_do())
           
            detach(user)

            return {"message": message}
        
    
@router.get("/goodbye", status_code=200)
async def goodbye():
    
    start_time = time.perf_counter()
    user_name = os.environ['NAME']
    
    user = attach(
        baggage.set_baggage("user.name", user_name)
    )
    with tracer.start_as_current_span("Greeting Request", attributes={ "Requires environment var": "NAME", "library":"FastAPI" } ):
        parent_context = baggage.set_baggage("user.id", "10002494")
        
        with tracer.start_as_current_span("Child Span", context=parent_context):
            child_context = baggage.set_baggage("role", "Performance Engineer")
            message = "Goodbye {} !. {}".format(user_name, another_thing_to_do())

            
            http_requests_counter.add(1)
            response_time = time.perf_counter() - start_time
            http_rt.record(response_time)
            
            detach(user)

            return {"message": message}
