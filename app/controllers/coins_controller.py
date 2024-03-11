import random
from fastapi import APIRouter, HTTPException
from app.instrumentation import metrics_exporter

router = APIRouter()

metrics = metrics_exporter.config('greetings-service')
meter = metrics.get_meter(__name__)

heads_count = meter.create_counter("heads_count")
tails_count = meter.create_counter("tails_count")
flip_count  = meter.create_counter("flip_count")

@router.get("/flip-coins", status_code=200)
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Times must be set in request and should be an Integer"
        )
    
    times_int = int(times)

    heads = 0
    for _ in range(times_int):
        if random.randint(0,1):
            heads += 1
    tails = times_int - heads

    heads_count.add(heads)
    tails_count.add(tails)
    flip_count.add(times_int)

    return {
        "heads": heads,
        "tails": tails,
    }