## Test counter for Hazelcast 5.4.0

### Prepare environment

```bash
cd ..
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cd task2/
docker compose up -d
```

### Run tests

```bash
# check memory
lsmem
# check CPUs
lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('
# start tests
python3 massive_counter_increment.py
```

### Docker commands

```bash
docker ps
# start tests
# test `without_locking`
# test `optimistic_locking`
# test `pessimistic_locking`
docker logs hz-1
docker stop hz-3
# test `optimistic_locking` without one container
# test `pessimistic_locking` without one container
docker start hz-3
# test `iatomiclong` 
docker stop hz-3
# test `iatomiclong` without NOT LEADER container
docker start hz-3
docker stop hz-1
# test `iatomiclong` without LEADER container
docker compose stop
# save logs
docker logs hz-1 > logs/hz-1.log
docker logs hz-2 > logs/hz-2.log
docker logs hz-3 > logs/hz-3.log
# down
docker compose down
```

### Links

- [Hazelcast Python Client](https://hazelcast.com/clients/python/)
- [Using Python Client with Hazelcast](https://hazelcast.readthedocs.io/en/stable/using_python_client_with_hazelcast.html)
- [Hazelcast in Docker](https://docs.hazelcast.com/hazelcast/5.1/getting-started/get-started-docker)
- [Docker compose samples](https://github.com/hazelcast/hazelcast-code-samples/blob/master/hazelcast-integration/docker-compose/00_vanilla/docker-compose.yml)

