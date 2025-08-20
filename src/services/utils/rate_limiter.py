import time
def token_bucket(rate_per_sec=0.5, capacity=5):
    tokens = capacity
    last = time.time()
    while True:
        now = time.time()
        tokens = min(capacity, tokens + (now - last) * rate_per_sec)
        last = now
        if tokens >= 1:
            tokens -= 1
            yield True
        else:
            time.sleep((1 - tokens) / rate_per_sec)
