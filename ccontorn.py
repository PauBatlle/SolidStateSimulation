import numpy as np

def inbox(x, v, limit = 1):
    v = v*np.sign(x)*np.sign(limit-x)
    return abs(limit-abs(x-limit)), v