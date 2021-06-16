from typing import Dict, Tuple, Union
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from redis import client
from redistimeseries.client import Client
import uvicorn
import time


from app.settings import Settings
from app.dependiens import get_client, validate_amount

config = Settings()

app = FastAPI(
    title="""REST Api using FastAPI development test for timeseries amount""",
    responses={403: {"description": "The amout over limiter",
                     "content": {
                         "application/json": {
                             "example": {"detail": "amount limit exeeded (1000/10sec)"}
                         }
                     },
                     }})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup():
    client = get_client(config)
    client.redis.flushdb()
    if not config.MULTI:
        delay = config.AMOUNT_LIMIT_1MIN*1000
    else:
        delay = 60000
    correlation = delay
    client.create('amount', retention_msecs=delay+correlation)


@app.get('/')
async def hello():
    return {'message': "hello"}


@app.get('/{amount}',
         status_code=200)
async def get_amount(redis_data: Tuple[int, Client] = Depends(validate_amount)):
    client, amount = redis_data
    client.add('amount', '*', amount)
    return {"result": "Ok"}


if __name__ == "__main__":
    uvicorn.run('main:app', host=config.APP_HOST,
                port=config.APP_PORT, workers=4,
                reload=config.RELOAD,
                log_level="info", debug=config.DEBUG)
