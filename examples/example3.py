import click
from pathlib import Path
import multiprocessing
import time
from itertools import repeat

lock = multiprocessing.Lock()

@click.command()
@click.option("--lock", is_flag=True)
def generator(lock):
    return zip(range(4), "abcd", repeat(lock))

def run(a, b, l):
    if l:
        lock.acquire()
        time.sleep(0.5)
        print(a,b)
        lock.release()
    else:
        time.sleep(0.5)
        print(a,b)
