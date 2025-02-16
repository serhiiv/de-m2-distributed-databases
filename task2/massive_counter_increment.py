import time
import hazelcast
import threading
from functools import wraps
from concurrent.futures import ThreadPoolExecutor


tread_local = threading.local()
WORKERS = 3
REPEAT = 100


def time_logger(func):
    """
    A decorator that logs the execution time of the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        # print(f"Function '{fname}' {result} took {end_time - start_time:.4f} seconds.")
        print(f"{result} took {end_time - start_time:.4f} seconds.")
        return result
    return wrapper


def hazelcast_connection(func):
    """
    A decorator that establishes a connection to a Hazelcast database
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        client = hazelcast.HazelcastClient(
            cluster_name="counter",
            cluster_members=["localhost:5702", "localhost:5701", "localhost:5703"]
            )
        output = func(client, *args, **kwargs)
        client.shutdown()
        return output
    return wrapper


@time_logger
def experiment(func) -> str:
    """
    Runs an experiment by executing a given function concurrently using a thread pool.
    """
    print("\n\n=== Start experiment")
    print(f"Function '{func.__name__}'")
    print(get_counter(func.__name__))
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(func, i) for i in range(WORKERS)]
        for future in futures:
            future.result()
    # print(check_counter())
    print(get_counter(func.__name__))
    print("=== The experiment", end="")
    return ""


@hazelcast_connection
def get_counter(client: hazelcast.HazelcastClient, map_name: str) -> str:
    # print(client.cluster_service.get_members())
    # print(client.cluster_service.get_cluster_id())
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
    init_map = client.get_map("locking_map")
    init_map.set("counter_locking_map", 0).result()
    init_map = client.get_map("optimistic_locking")
    init_map.set("counter_optimistic_locking", 0).result()
    init_map = client.get_map("optimistic_locking_without_node")
    init_map.set("counter_optimistic_locking_without_node", 0).result()
    init_map = client.get_map("pessimistic_locking")
    init_map.set("counter_pessimistic_locking", 0).result()
    init_map = client.get_map("pessimistic_locking_without_node")
    init_map.set("counter_pessimistic_locking_without_node", 0).result()
    return "Initialization completed."

# distributed_map


# locking_map
@hazelcast_connection
@time_logger
def locking_map(client: hazelcast.HazelcastClient, tread_id: int, map_name: str = "locking_map") -> str:
    work_map = client.get_map(map_name).blocking()
    key = "counter_" + map_name

    for _ in range(REPEAT):
        counter = work_map.get(key)
        counter += 1
        work_map.put(key, counter)

    return f"tread {tread_id} with counter {counter}"


# # pessimistic_locking
# @hazelcast_connection
# @time_logger
# def pessimistic_locking(client, tread_id: int, map_name: str = "pessimistic_locking") -> str:
#     work_map = client.get_map(map_name).blocking()
#     key = "counter_" + map_name

#     for _ in range(REPEAT):
#         work_map.lock(key)
#         try:
#             counter = work_map.get(key)
#             counter += 1
#             work_map.put(key, counter)
#         finally:
#             work_map.unlock(key)

#     return f"tread {tread_id} with counter {counter}"


# optimistic_locking
# pessimistic_locking_without_node
# optimistic_locking_without_node
# iatomiclong
# iatomiclong_without_lider


if __name__ == "__main__":
    print(init_maps())
    # experiment(distributed_map)
    experiment(locking_map)
    # experiment(pessimistic_locking)
    # experiment(optimistic_locking)
    # experiment(pessimistic_locking_without_node)
    # experiment(optimistic_locking_without_node)
    # experiment(iatomiclong)
    # experiment(iatomiclong_without_lider)
