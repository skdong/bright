from functools import wraps

def bubble(arry):
    n = len(arry)
    while n > 1:
        for i in range(n-1):
            if arry[i] > arry[i+1]:
                arry[i], arry[i+1] = arry[i+1], arry[i]
                n = i + 1






def print_log(f):
    @wraps(f)
    def func(*args, **kwargs):
        print 'a'
        f(*args, **kwargs)
        print 'b'
    return func

@print_log
def test_print(a, b):
    print a,b
    print 'test'

def check_deractor():
    test_print(1,2)
    print test_print.__name__

def test_range(n):
    for i in range(n):
        yield  i

def check_range():
    for i in test_range(10):
        print i


class 