## Counter implementation using PostgreSQL

It is necessary to implement straightforward functionality that is part of social networks, video platforms, photo and video-sharing services, etc. This functionality is a counter of likes/views/retweets …, which increases by one when a corresponding action is taken.



### Run Postgres Docker

```bash
./run_postgres_docker.sh 
docker ps
```

### Prepear environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Testing implementation options

```bash
`lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('`
python3 massive-insert.py
```

### Clear Docker

```bash
docker ps
docker stop ...
docker rm ...
docker image ls
docker rmi ...
```
