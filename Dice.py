import random
def dice(size, times=None):
    if not times:
        return random.randint(1,size)
    else:
        return [random.randint(1,size) for _ in range(times)]

def d100(times=None):
    return dice(100, times)
def d20(times=None):
    return dice(20, times)
def d10(times=None):
    return dice(10, times)
def d8(times=None):
    return dice(8, times)
def d6(times=None):
    return dice(6, times)
def d4(times=None):
    return dice(4, times)

def mutable(parameter, default_val):
    if parameter is None:
        return default_val
    else:
        return parameter
