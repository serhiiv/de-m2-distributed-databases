import time
import hazelcast  # type: ignore
import threading
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

# Create a thread-local object to store the Hazelcast client.
tread_local = threading.local()

WORKERS = 10
REPEAT = 10000


def time_logger(func):
    """
    A decorator that logs the execution time of the decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        output = func(*args, **kwargs)
        print(f"{output} took {time.perf_counter() - start_time:.4f} seconds.")
        return output

    return wrapper


def hazelcast_connection(func):
    """
    A decorator that establishes a connection to a Hazelcast database
    """

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
    """
    Runs an experiment by executing a given function concurrently using a thread pool.
    """
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
    """
    Get counter
    """
    if func_name == "iatomiclong":
        atomic_long = client.cp_subsystem.get_atomic_long("counter").blocking()
        counter = atomic_long.get()
    else:
        counter_map = client.get_map("experiment").blocking()
        counter = counter_map.get("counter")
    return f"{"experiment"} counter = {counter}"


@hazelcast_connection
def init_counter(client: hazelcast.HazelcastClient, func_name: str) -> str:
    """
    Initialize counter
    """
    if func_name == "iatomiclong":
        atomic_long = client.cp_subsystem.get_atomic_long("counter").blocking()
        atomic_long.set(0)
    else:
        init_map = client.get_map("experiment")
        init_map.set("counter", 0).result()
    return f"Initialization counter for '{func_name}'."


@hazelcast_connection
@time_logger
def map_without_locking(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    """
    Counter without locking
    """
    work_map = client.get_map("experiment").blocking()
    for _ in range(REPEAT):
        counter = work_map.get("counter")
        counter += 1
        work_map.put("counter", counter)
    return f"tread {tread_id} with counter {counter}"


@hazelcast_connection
@time_logger
def pessimistic_locking(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    """
    Counter with pessimistic locking
    """
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


@hazelcast_connection
@time_logger
def optimistic_locking(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    """
    Counter with optimistic locking
    """
    work_map = client.get_map("experiment").blocking()
    for _ in range(REPEAT):
        while True:
            counter = work_map.get("counter")
            if work_map.replace_if_same("counter", counter, counter + 1):
                counter += 1
                break
    return f"tread {tread_id} with counter {counter}"


@hazelcast_connection
@time_logger
def iatomiclong(client: hazelcast.HazelcastClient, tread_id: int) -> str:
    """
    Counter using IAtomicLong and enabling CP Sysbsystem
    """
    atomic_long = client.cp_subsystem.get_atomic_long("counter").blocking()
    for _ in range(REPEAT):
        counter = atomic_long.increment_and_get()
    return f"tread {tread_id} with counter {counter}"


if __name__ == "__main__":
    """
    Run experiments with different locking strategies.
    """
    experiment(map_without_locking)

    experiment(pessimistic_locking)
    experiment(optimistic_locking)

    print("\n\nStop ANY container end")
    input("Press Enter to continue...")
    experiment(pessimistic_locking)
    experiment(optimistic_locking)

    print("\n\nStart previous container and")
    input("Press Enter to continue...")
    experiment(iatomiclong)

    print("\n\nStop LEADER container and")
    input("Press Enter to continue...")
    experiment(iatomiclong)
