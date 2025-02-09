import time
import psycopg2
import threading
from psycopg2 import OperationalError
from concurrent.futures import ThreadPoolExecutor

DSN = "host=127.0.0.1 port=5432 dbname=postgres user=root password=secret"
tread_local = threading.local()


def time_logger(func):
    """
    A decorator that logs the execution time of the decorated function.
    """
    fname = str(func.__name__)

    def wrapper2(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function '{fname}' {result} took {end_time - start_time:.4f} seconds.")
        return result

    return wrapper2


def postgres(func):
    """
    A decorator that establishes a connection to a PostgreSQL database using the DSN (Data Source Name),
    creates a cursor, and passes them to the decorated function.
    """

    def wrapper(*args, **kwargs):
        connect = psycopg2.connect(DSN)
        cursor = connect.cursor()
        result = func(connect, cursor, *args, **kwargs)
        cursor.close()
        connect.close()
        return result

    return wrapper


@postgres
def create_table(connect, cursor):
    """
    Drops the table `user_counter` if it exists, creates a new `user_counter` table,
    and inserts an initial row with counter and version set to 0 for the user with user_id = 1.
    """
    cursor.execute("""
    drop table if exists user_counter;
    create table user_counter (
        user_id serial primary key
        , counter integer
        , version integer
    );
    insert into user_counter (counter, version) values (0, 0);
    """
    )
    connect.commit()
    return "Clear table `user_counter`."


@postgres
def check_counter(connect, cursor) -> str:
    """
    Retrieves the counter value for a specific user from the database.
    """
    cursor.execute("select counter from user_counter where user_id = 1;")
    counter = cursor.fetchone()[0]
    return f"Counter value is {counter}."


@time_logger
def experiment(func) -> str:
    """
    Runs an experiment by executing a given function concurrently using a thread pool.
    """
    print("\n\n=== Start experiment ===")
    print(create_table())
    print(check_counter())

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(func, i) for i in range(10)]
        for future in futures:
            future.result()

    print(check_counter())
    return ""


@postgres
@time_logger
def lost_update(connect, cursor, tread_id: int) -> str:
    """
    Simulates a lost update scenario by incrementing a counter in a database table.
    This function demonstrates a lost update problem by reading a counter value,
    incrementing it, and writing it back to the database without proper locking
    mechanisms, which can lead to race conditions in a concurrent environment.
    """
    for _ in range(10):
        cursor.execute("select counter from user_counter where user_id = 1;")
        counter = cursor.fetchone()[0]
        counter += 1
        cursor.execute(
            f"update user_counter set counter = {counter} where user_id = 1;"
        )
        connect.commit()
    return f"tread {tread_id} with counter {counter}"


@postgres
@time_logger
def lost_update_serializable(connect, cursor, tread_id):
    """
    Executes a series of updates on a counter in a PostgreSQL database using the SERIALIZABLE isolation level.
    """
    connect.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    for _ in range(10):
        while True:
            try:
                cursor.execute("select counter from user_counter where user_id = 1;")
                counter = cursor.fetchone()[0]
                counter += 1
                cursor.execute(
                    f"update user_counter set counter = {counter} where user_id = 1;"
                )
                connect.commit()
                break
            except OperationalError as e:
                if e.pgcode != "40001":
                    raise
                # Serialization failure
                connect.rollback()
    return f"tread {tread_id} with counter {counter}"


@postgres
@time_logger
def in_place_update(connect, cursor, tread_id):
    """
    This function performs an in-place update on the user_counter table by incrementing
    the counter for the user with user_id = 1.
    """
    for _ in range(10):
        cursor.execute("update user_counter set counter = counter+1 where user_id = 1;")
        connect.commit()
    return f"tread {tread_id}"


@postgres
@time_logger
def row_level_locking(connect, cursor, tread_id):
    """
    Perform row-level locking to increment a counter in a database table.
    """
    for _ in range(10):
        cursor.execute("select counter from user_counter where user_id = 1 for update;")
        counter = cursor.fetchone()[0]
        counter += 1
        cursor.execute(
            f"update user_counter set counter = {counter} where user_id = 1;"
        )
        connect.commit()
    return f"tread {tread_id} with counter {counter}"


@postgres
@time_logger
def optimistic_concurrency_control(connect, cursor, tread_id):
    """
    Perform an optimistic concurrency control update on a user counter.
    """
    for _ in range(10):
        while True:
            cursor.execute(
                "select counter, version from user_counter where user_id = 1;"
            )
            counter, version = cursor.fetchone()
            counter += 1
            cursor.execute(
                f"""
            update user_counter set counter = {counter}, version = {version + 1}
            where user_id = 1 and version = {version}
            """
            )
            connect.commit()
            if cursor.rowcount > 0:
                break
    return f"tread {tread_id} with counter {counter}"


if __name__ == "__main__":
    print("")
    experiment(lost_update)
    experiment(lost_update_serializable)
    experiment(in_place_update)
    experiment(row_level_locking)
    experiment(optimistic_concurrency_control)
