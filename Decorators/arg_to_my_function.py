from datetime import datetime
from functools import wraps

def log_datetime(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print(f'Function: {func.__name__}\nRun on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{"-"*30}')
        func(*args,*kwargs)

    return wrapper

@log_datetime
def my_func(my_arg):
    '''Simple decorator testing'''
    print(my_arg)

my_func("this is my statement")        
print(my_func.__name__)
print(my_func.__doc__)