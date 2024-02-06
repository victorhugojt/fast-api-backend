from fastapi import APIRouter, HTTPException, Response
import os
import random
import prometheus_client


router = APIRouter()

heads_count = prometheus_client.Counter(
    "heads_count", "Number of heads"
)

tails_count = prometheus_client.Counter(
    "tails_count", "Number of tails"
)

flip_count = prometheus_client.Counter(
    "flip_count", "Number of flips"
)

@router.get("/", status_code=200)
async def info():
    return {"message": "Ready"}


@router.get("/ping", status_code=200)
async def info():
    return {"pong !"}


@router.get("/hi", status_code=200)
async def greeting():
    name = os.environ['NAME']
    return {"message": "Hello {} !".format(name)}


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

    heads_count.inc(heads)
    tails_count.inc(tails)
    flip_count.inc(times_int)

    return {
        "heads": heads,
        "tails": tails,
    }

@router.get("/metrics", status_code=200)
def get_metrics():
    return Response( content=prometheus_client.generate_latest(), media_type="text/plain")


