from time import perf_counter
from logger import get_logger


def get_performance_metric(func):
    def wrapper(*args,**kwargs):
        start_time = perf_counter()
        try:
            func(*args, **kwargs)
        except Exception as exception:
            raise exception
        finally:
            end_time = perf_counter()
            total_time = round(end_time - start_time, 2)
            print("process time : {} seconds | func name : ({})".format(total_time, func.__name__).upper())
    return wrapper


def get_performance_metric_info_log(func):
    logger = get_logger('performance_metric')
    def wrapper(*args,**kwargs):
        start_time = perf_counter()
        try:
            func(*args, **kwargs)
        except Exception as exception:
            raise exception
        finally:
            end_time = perf_counter()
            total_time = round(end_time - start_time, 2)
            logger.info("process time : {} seconds | func name : ({})".format(total_time, func.__name__).upper())
    return wrapper
