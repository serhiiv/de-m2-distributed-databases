import time
import psycopg2
import threading
from psycopg2 import OperationalError
from concurrent.futures import ThreadPoolExecutor

DSN = "host=127.0.0.1 port=5432 dbname=postgres user=root password=secret"
tread_local = threading.local()


def experiment(func):
    print(f"\n\n=== Experiment {func.__name__.upper()} ===")
    create_table()
    check_counter()
    print("Threads start")
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(func, i) for i in range(10)]
        for future in futures:
            future.result()

    run_time = time.perf_counter() - start_time
    print("Threads end")
    print(f"All threads finished in {run_time:.4f} seconds")
    check_counter()


def create_table():
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    cur.execute("""
    drop table if exists user_counter;
    create table user_counter (
        user_id serial primary key
        , counter integer
        , version integer
    );
    insert into user_counter (counter, version) values (0, 0);
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Clear table `user_counter`")


def check_counter():
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    cur.execute("select counter from user_counter where user_id = 1;")
    counter = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"Current counter value is {counter}")


def lost_update(tread_id):
    start_time = time.perf_counter()

    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    for _ in range(10000):
        cur.execute("select counter from user_counter where user_id = 1;")
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute(f"update user_counter set counter = {counter} where user_id = 1;")
        conn.commit()
    cur.close()
    conn.close()

    run_time = time.perf_counter() - start_time
    print(f"tread {tread_id} with counter {counter} finished in {run_time:.4f} seconds")


def lost_update_serializable(tread_id):
    start_time = time.perf_counter()
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    cur.execute("set transaction isolation level serializable;")
    for _ in range(10000):
        while True:
            try:
                cur.execute("select counter from user_counter where user_id = 1;")
                counter = cur.fetchone()[0]
                counter += 1
                cur.execute(f"update user_counter set counter = {counter} where user_id = 1;")
                conn.commit()
                break
            except OperationalError as e:
                if e.pgcode == '40001':  # Serialization failure
                    conn.rollback()
                else:
                    raise
    cur.close()
    conn.close()

    run_time = time.perf_counter() - start_time
    print(f"tread {tread_id} with counter {counter} finished in {run_time:.4f} seconds")


def in_place_update(tread_id):
    start_time = time.perf_counter()

    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    for _ in range(10000):
        cur.execute("update user_counter set counter = counter+1 where user_id = 1;")
        conn.commit()
    cur.close()
    conn.close()

    run_time = time.perf_counter() - start_time
    print(f"tread {tread_id} finished in {run_time:.4f} seconds")


def row_level_locking(tread_id):
    start_time = time.perf_counter()

    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    for _ in range(10000):
        cur.execute("select counter from user_counter where user_id = 1 for update;")
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute(f"update user_counter set counter = {counter} where user_id = 1;")
        conn.commit()
    cur.close()
    conn.close()

    run_time = time.perf_counter() - start_time
    print(f"tread {tread_id} with counter {counter} finished in {run_time:.4f} seconds")


def optimistic_concurrency_control(tread_id):
    start_time = time.perf_counter()

    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    for _ in range(10000):
        while True:
            cur.execute("select counter, version from user_counter where user_id = 1;")
            counter, version = cur.fetchone()
            counter += 1
            cur.execute(f"""update user_counter set counter = {counter},
            version = {version + 1} where user_id = 1 and version = {version}""")
            conn.commit()
            count = cur.rowcount
            if count > 0:
                break
    cur.close()
    conn.close()

    run_time = time.perf_counter() - start_time
    print(f"tread {tread_id} with counter {counter} finished in {run_time:.4f} seconds")


if __name__ == '__main__':
    experiment(lost_update)
    experiment(lost_update_serializable)
    experiment(in_place_update)
    experiment(row_level_locking)
    experiment(optimistic_concurrency_control)
