import time
import threading
from neo4j import GraphDatabase
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

# Create a thread-local object to store the Hazelcast client.
tread_local = threading.local()

WORKERS = 10
REPEAT = 10000
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j_password")


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


def neo4j_connection(func):
    """
    A decorator that establishes a connection to a neo4j database
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        driver = GraphDatabase.driver(URI, auth=AUTH)
        session = driver.session(database="neo4j")
        output = func(session, *args, **kwargs)
        session.close()
        driver.close()
        return output

    return wrapper


@neo4j_connection
def get_random_item(session) -> str:
    """
    Initialize counter
    """
    result = session.run(
        """
        MATCH (i:Item)
        WITH i, rand() as r ORDER BY r LIMIT 1
        RETURN i.name as item;
        """
    )
    return result.value("item")[0]


@neo4j_connection
def init_like_counter(session, item: str) -> str:
    session.run(
        f"""
        MATCH (i:Item {{name: "{item}"}})
        SET i.like = 0
        RETURN i.like as counter;
        """
    )
    return f"\nInitialization counter for item '{item}'."


@neo4j_connection
def get_like_counter(session, item: str) -> str:
    result = session.run(
        f"""
        MATCH (i:Item {{name: "{item}"}})
        RETURN i.like as counter;
        """
    )
    counter = result.value("counter")[0]
    return f"\nCounter for item '{item}' is equal to {counter}."


@neo4j_connection
@time_logger
def make_likes(session, treade_id: int, item: str) -> str:
    for _ in range(REPEAT):
        result = session.run(
            f"""
            MATCH (i:Item {{name: "{item}"}})
            SET i.like = i.like + 1
            RETURN i.like as counter;
            """
        )
        counter = result.value("counter")[0]
    return f"tread {treade_id} for item '{item}' with counter {counter}"


@time_logger
def experiment() -> str:
    """
    Runs an experiment by executing a given function concurrently using a thread pool.
    """
    item = get_random_item()
    print(f"\n\n=== Start experiment for '{item}':")
    print(init_like_counter(item))
    print(get_like_counter(item))
    print()

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(make_likes, i, item) for i in range(WORKERS)]
        for future in futures:
            future.result()

    print(get_like_counter(item))
    return f"\n=== The experiment for '{item}' is over and"


if __name__ == "__main__":
    experiment()
