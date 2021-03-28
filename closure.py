# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:31:15 2019

@author: Administrator
"""

class Avg:
    def __init__(self):
        self.values = []
    def __call__(self, value):
        self.values.append(value)
        return sum(self.values) / len(self.values)
avg = Avg()
avg(10)
avg(11)
avg(12)

def outer():
    values = []
    def memorize_values(value):
        values.append(value)
        return sum(values) / len(values)
    return memorize_values

avg = outer()
avg(10)
avg(11)
avg(12)


def outer():
    sum_ = 0
    cnt = 0
    def memorize_sum_and_count(value):
        nonlocal sum_, cnt
        sum_ += value
        cnt += 1
        return sum_ / cnt
    return memorize_sum_and_count

avg = outer()
avg(10)
avg(11)
avg(12)

def fbnc():
    history = [1, 1]
    def wrapper(n):
        if n > len(history):
            res = wrapper(n-1) +  wrapper(n-2)
            history.append(res)
            return res
        else:
            print("no compute")
            return history[n - 1]
    return wrapper
        
# 使用协程
def make_average():
    sum_ = 0
    cnt = 0
    while True:
        sum_ += yield
        cnt += 1
        yield sum_ / cnt

avg = make_average()
next(avg)  # 启动
avg.send(10)   # yield均值后暂停
next(avg)
avg.send(11)
next(avg)
avg.send(12)

# 上面的方式太冗余了，两个yield暂停两次，优化下
def make_average():
    sum_ = 0
    cnt = 0
    avg = "non_meaning"
    while True:
        value = yield avg
        sum_ += value
        cnt += 1
        avg = sum_ / cnt
avg = make_average()

res1 = next(avg)        # 启动至yield，产生avg，暂停等待send； res1是“non_meaning”
res2 = avg.send(10)
res3 = avg.send(11)
res4 = avg.send(12)

# 预激生成器
from functools import wraps
def pre_active(gen):
    @wraps(gen)
    def wrapper(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return wrapper

@pre_active
def make_average():
    sum_ = 0
    cnt = 0
    avg = None
    while True:
        value = yield avg
        sum_ += value
        cnt += 1
        avg = sum_ / cnt
avg = make_average()
avg.send(10)
avg.send(11)
avg.send(12)