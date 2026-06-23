import time
import random

def polite_sleep(min_s = 2.0, max_s = 6.0):
    delay = random.uniform(min_s, max_s)
    print(f"  [rate-limit] sleeping {delay:.2f}s …")
    time.sleep(delay)
