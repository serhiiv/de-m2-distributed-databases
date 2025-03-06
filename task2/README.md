## Test counter for Hazelcast

### Prepare environment

```bash
cd ..
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cd task2
docker compose up -d
```

### Run tests

```bash
# check memory
lsmem
# check CPUs
$ lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('
# start tests
python3 massive_counter_increment.py
```


### Links

[https://gamov.io/posts/2017/06/08/how-to-scale-hazelcast-docker-containers-with-docker-compose.html](URL)

[https://github.com/hazelcast/hazelcast-code-samples/blob/master/hazelcast-integration/docker-compose/00_vanilla/docker-compose.yml](https://github.com/hazelcast/hazelcast-code-samples/blob/master/hazelcast-integration/docker-compose/00_vanilla/docker-compose.yml)

### 
