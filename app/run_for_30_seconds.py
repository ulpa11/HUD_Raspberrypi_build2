import time

def run_for_30_seconds():
    start_time = time.time()
    while True:
        if time.time() - start_time > 30:
            break
        # do something here