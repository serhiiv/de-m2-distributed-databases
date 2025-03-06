import time
# import logging
import hazelcast  # type: ignore
import threading
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

# # Enable logging to see the logs
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("hazelcast")
# logger.setLevel(logging.ERROR)

# handler = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# Create a thread-local object to store the Hazelcast client.
tread_local = threading.local()

WORKERS = 3
REPEAT = 100


def time_logger(func):
    # A decorator that logs the execution time of the decorated function.
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        output = func(*args, **kwargs)
        print(f"{output} took {time.perf_counter() - start_time:.4f} seconds.")
        return output

    return wrapper


def hazelcast_connection(func):
    # A decorator that establishes a connection to a Hazelcast database
    @wraps(func)
    def wrapper(*args, **kwargs):
        client = hazelcast.HazelcastClient(
            cluster_name="counter",
            cluster_members=["localhost:5702", "localhost:5701", "localhost:5703"],
        )
        output = func(client, *args, **kwargs)
        client.shutdown()
        return output

    return wrapper


@time_logger
# @hazelcast_connection
def experiment(func) -> str:
    # Runs an experiment by executing a given function concurrently using a thread pool.
    print("\n\n=== Start experiment")
    print(f"Function '{func.__name__}'")
    print(init_counter(func.__name__))
    print(get_counter(func.__name__))
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(func, i) for i in range(WORKERS)]
        for future in futures:
            future.result()
    print(get_counter(func.__name__))
    return f"=== The experiment '{func.__name__}'"


@hazelcast_connection
def get_counter(client: hazelcast.HazelcastClient, func_name: str) -> str:
    if func_name == "iatomiclong":
        pass
    else:
        counter_map = client.get_map("experiment").blocking()
        counter = counter_map.get("counter")
    return f"{"experiment"} counter = {counter}"


@hazelcast_connection
def init_counter(client: hazelcast.HazelcastClient, func_name: str) -> str:
    if func_name == "iatomiclong":
        pass
    else:
        init_map = client.get_map("experiment")
        init_map.set("counter", 0).result()
    return f"Initialization counter for '{func_name}'."


# map_without_locking
@hazelcast_connection
@time_logger
def map_without_locking(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    work_map = client.get_map("experiment").blocking()
    for _ in range(REPEAT):
        counter = work_map.get("counter")
        counter += 1
        work_map.put("counter", counter)
    return f"tread {tread_id} with counter {counter}"


# pessimistic_locking
@hazelcast_connection
@time_logger
def pessimistic_locking(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    work_map = client.get_map("experiment").blocking()
    for _ in range(REPEAT):
        work_map.lock("counter")
        try:
            counter = work_map.get("counter")
            counter += 1
            work_map.put("counter", counter)
        finally:
            work_map.unlock("counter")
    return f"tread {tread_id} with counter {counter}"


# optimistic_locking
@hazelcast_connection
@time_logger
def optimistic_locking(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    work_map = client.get_map("experiment").blocking()
    for _ in range(REPEAT):
        while True:
            counter = work_map.get("counter")
            if work_map.replace_if_same("counter", counter, counter + 1):
                counter += 1
                break
    return f"tread {tread_id} with counter {counter}"


# iatomiclong
@hazelcast_connection
@time_logger
def iatomiclong(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    work_map = client.g
    counter = work_map.get("counter")
    for _ in range(REPEAT):
        counter += 1
    work_map.put("counter", counter)
    return f"tread {tread_id} with counter {counter}"


if __name__ == "__main__":

    experiment(map_without_locking)

    experiment(pessimistic_locking)
    experiment(optimistic_locking)

    # experiment(iatomiclong)
