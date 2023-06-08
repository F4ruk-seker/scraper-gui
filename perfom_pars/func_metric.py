from time import perf_counter


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
            print(f"process time : {total_time} seconds | func name : ({func.__name__})".upper())
    return wrapper




