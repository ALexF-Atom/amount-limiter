from typing import Dict
from fastapi import Path, Depends, HTTPException
from .settings import Settings
from redistimeseries.client import Client
from functools import lru_cache
import time


@lru_cache
def get_config():
    return Settings()


def get_client(config: Settings = Depends(get_config)):
    client = Client(host=config.REDIS_HOST,
                    port=config.REDIS_PORT,
                    db=0)
    return client


def get_limits(config: Settings = Depends(get_config)):
    if not config.MULTI:
        key = {10: config.AMOUNT_LIMIT_10SEC, 60: config.AMOUNT_LIMIT_1MIN}
    else:
        key = {}
    return key


async def validate_amount(amount: int = Path(...),
                          client: Client = Depends(get_client),
                          limits: Dict[int, int] = Depends(get_limits)):
    for key,limit in limits.items():
        res = get_(client, key*1000)
        if res:
            res = sum(i[1] for i in res)
        else:
            res = 0
        if amount + res > limit:
            raise HTTPException(status_code=403, detail=f'"amount limit exeeded ({limit}/{key}sec)"')

    
    return client, amount

        


def get_(client, correlation):
    tim = int(time.time()*1000)
    return client.range('amount', from_time=tim-correlation, to_time=tim,
                        aggregation_type='sum', bucket_size_msec=correlation)
