import time
import asyncio
import datetime
import pytz


def time_me(func):

    def inner(*args, **kwargs):
        start_time: float = time.time()

        # Calls function that is wrapped by the decorator
        return_result = func(*args, **kwargs)

        end_time: float = time.time()

        print(f"{func.__name__} ran for {end_time - start_time} seconds.")
        
        return return_result

    return inner

def background_task(interval_seconds: int=0, delay_task: bool=False):
    """If delay_task is set to True, it goes through the delay for inverval_seconds first"""
    
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if not delay_task:
                await func(*args, **kwargs)

            while True:
                await asyncio.sleep(interval_seconds)
                await func(*args, **kwargs)

        return wrapper

    return decorator

def daily_task(hour: int=0, minute: int=0, 
               second: int=0, microsecond: int=0, 
               time_zone: str=pytz.timezone(r"US/Eastern")):
    """Repeats an assync task once a day at the specified time"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            while True:
                current_time = datetime.datetime.now(time_zone)
                task_time = current_time.replace(
                    hour=hour, 
                    minute=minute, 
                    second=second, 
                    microsecond=microsecond
                )
                
                # If the target time has already passed for today, schedule it for tomorrow
                if current_time >= task_time:
                    task_time += datetime.timedelta(days=1)
                
                time_until_target = (task_time - current_time).total_seconds()
                
                await asyncio.sleep(time_until_target)
                await func(*args, **kwargs)

        return wrapper
    
    return decorator
