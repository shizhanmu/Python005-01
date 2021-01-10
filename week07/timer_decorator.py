import time

def timer(func):
    def inner(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        timedelta = time.time() - start
        print(f"函数 {func.__name__} 运行时间：{timedelta}")
        return ret
    return inner

@timer
def myfunc(x, y):
    print("start running myfunc")
    print(x * 3, y + 5)
    time.sleep(2)
    print("finished running myfunc")

myfunc(2, 3)