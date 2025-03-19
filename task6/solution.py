import time
import datetime
import threading
import subprocess
from pymongo import MongoClient, WriteConcern
from pymongo.errors import AutoReconnect
from functools import wraps
from concurrent.futures import ThreadPoolExecutor


# Create a thread-local object to store the Hazelcast client.
tread_local = threading.local()

WORKERS = 10
REPEAT = 10000
URI = "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0"


def now():
    return datetime.datetime.now().time()


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


def mongodb_connection(func):
    """
    A decorator that establishes a connection to a MongoDB
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        client = MongoClient(URI)
        db = client.task6
        collection = db.grades
        output = func(collection, *args, **kwargs)
        client.close()
        return output

    return wrapper


@mongodb_connection
def init_collection(collection) -> str:
    collection.drop()
    collection.insert_one({"name": "MongoDB", "like": 0})
    return f"{now()}   Initialize 'grades' collection"


@mongodb_connection
def get_like_counter(collection) -> str:
    counter = collection.find_one({"name": "MongoDB"})["like"]
    return f"{now()}   Likes for 'MongoDB' is equal to {counter}."


@mongodb_connection
@time_logger
def make_likes(collection, treade_id: int, wc: str | int) -> str:
    if wc != "majority":
        wc = int(wc)
    collection = collection.with_options(write_concern=WriteConcern(w=wc))
    for _ in range(REPEAT):
        try:
            counter = collection.find_one_and_update(
                {"name": "MongoDB"}, {"$inc": {"like": 1}}
            )["like"]
        except AutoReconnect:
            print(f"{now()}   AutoReconnect error, retrying...")
            time.sleep(0.1)  # Wait a bit before retrying

    return f"{now()}   tread {treade_id} for item 'MongoDB' with counter {counter}"


def get_primary_node_name() -> str | None:
    client: MongoClient = MongoClient(URI)
    client.is_primary
    if client.primary:
        ip, port = client.primary
        address = port - 27016
        return f"mongo{address}"
    return None


def disconnect_primary_node(container: str | None, delay_in_seconds: int) -> None:
    if container and delay_in_seconds > 0:
        time.sleep(delay_in_seconds)
        print(
            f"{now()}   Disconnect the node '{container}' after {delay_in_seconds} seconds after the start."
        )
        subprocess.run(["docker", "network", "disconnect", "mongoCluster", container])


def connect_node(container: str | None, delay_in_seconds: int) -> None:
    if container and delay_in_seconds > 0:
        print(f"{now()}   Connected the node '{container}'.")
        subprocess.run(["docker", "network", "connect", "mongoCluster", container])


@time_logger
def experiment(delay_in_seconds: int, writeConcern: str | int) -> str:
    """
    Runs an experiment by executing a given function concurrently using a thread pool.
    """
    primary_node = get_primary_node_name()
    print(f"\n\n\n{now()}   === Start experiment :")
    print("                  primary node :", primary_node)
    print("                  writeConcern :", writeConcern)
    print("                  delay in sec :", delay_in_seconds)
    print(init_collection())
    print(get_like_counter())

    with ThreadPoolExecutor(max_workers=WORKERS + 1) as executor:
        futures = [executor.submit(make_likes, i, writeConcern) for i in range(WORKERS)]
        if delay_in_seconds > 0:
            futures.append(
                executor.submit(disconnect_primary_node, primary_node, delay_in_seconds)
            )

        for future in futures:
            future.result()

    print(get_like_counter())
    connect_node(primary_node, delay_in_seconds)

    return f"{now()}   === The experiment is over and"


if __name__ == "__main__":

    experiment(delay_in_seconds=0, writeConcern=1)
    experiment(delay_in_seconds=0, writeConcern="majority")
    experiment(delay_in_seconds=1, writeConcern=1)
    time.sleep(10)
    experiment(delay_in_seconds=1, writeConcern="majority")
