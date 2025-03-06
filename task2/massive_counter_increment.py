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
def experiment(func) -> None:
    # Runs an experiment by executing a given function concurrently using a thread pool.
    print("\n\n=== Start experiment")
    print(f"Function '{func.__name__}'")
    print(get_counter(func.__name__))
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(func, i) for i in range(WORKERS)]
        for future in futures:
            future.result()
    print(get_counter(func.__name__))
    print("=== The experiment", end="")


@hazelcast_connection
def get_counter(client: hazelcast.HazelcastClient, map_name: str) -> str:
    counter_map = client.get_map(map_name).blocking()
    counter = counter_map.get("counter_" + map_name)
    return f"'counter_{map_name}' =  {counter}"


@hazelcast_connection
def init_maps(client: hazelcast.HazelcastClient) -> str:
    init_map = client.get_map("distributed_map")
    init_map.set("counter_distributed_map", 0).result()
    init_map = client.get_map("iatomiclong")
    init_map.set("counter_iatomiclong", 0).result()
    init_map = client.get_map("iatomiclong_without_lider")
    init_map.set("counter_iatomiclong_without_lider", 0).result()
    init_map = client.get_map("map_without_locking")
    init_map.set("counter_map_without_locking", 0).result()
    init_map = client.get_map("optimistic_locking")
    init_map.set("counter_optimistic_locking", 0).result()
    init_map = client.get_map("optimistic_locking_without_node")
    init_map.set("counter_optimistic_locking_without_node", 0).result()
    init_map = client.get_map("pessimistic_locking")
    init_map.set("counter_pessimistic_locking", 0).result()
    init_map = client.get_map("pessimistic_locking_without_node")
    init_map.set("counter_pessimistic_locking_without_node", 0).result()
    return "Initialization completed."


# map_without_locking
@hazelcast_connection
@time_logger
def map_without_locking(client: hazelcast.HazelcastClient, tread_id: int, map_name: str = "map_without_locking") -> str:
    work_map = client.get_map(map_name).blocking()
    key = "counter_" + map_name
    for _ in range(REPEAT):
        counter = work_map.get(key)
        counter += 1
        work_map.put(key, counter)
    return f"tread {tread_id} with counter {counter}"


# pessimistic_locking
@hazelcast_connection
@time_logger
def pessimistic_locking(client: hazelcast.HazelcastClient, tread_id: int, map_name: str = "pessimistic_locking") -> str:
    work_map = client.get_map(map_name).blocking()
    key = "counter_" + map_name
    for _ in range(REPEAT):
        work_map.lock(key)
        try:
            counter = work_map.get(key)
            counter += 1
            work_map.put(key, counter)
        finally:
            work_map.unlock(key)
    return f"tread {tread_id} with counter {counter}"


# optimistic_locking
@hazelcast_connection
@time_logger
def optimistic_locking(client: hazelcast.HazelcastClient, tread_id: int, map_name: str = "optimistic_locking") -> str:
    work_map = client.get_map(map_name).blocking()
    key = "counter_" + map_name
    for _ in range(REPEAT):
        while True:
            counter = work_map.get(key)
            if work_map.replace_if_same(key, counter, counter + 1):
                counter += 1
                break
    return f"tread {tread_id} with counter {counter}"


# iatomiclong
@hazelcast_connection
@time_logger
def iatomiclong(client: hazelcast.HazelcastClient, tread_id: int, map_name: str = "iatomiclong") -> str:
    work_map = client.g
    # get_map(map_name).blocking()
    key = "counter_" + map_name
    counter = work_map.get(key)
    for _ in range(REPEAT):
        counter += 1
    work_map.put(key, counter)
    return f"tread {tread_id} with counter {counter}"


if __name__ == "__main__":
    print(init_maps())

    experiment(map_without_locking)

    experiment(pessimistic_locking)
    experiment(optimistic_locking)

    # experiment(iatomiclong)
