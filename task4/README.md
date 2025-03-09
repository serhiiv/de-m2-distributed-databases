## Test counter for Hazelcast 5.4.0

### Prepare environment

```bash
cd ..
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cd task4/
docker compose up -d
sleep 5
# check Neo4j Browser
docker logs neo4j
```

### Test #1

Open Neo4j Browser [http://localhost:7474/](http://localhost:7474/) and execute file `protocol.cypher`

### Test #2

```bash
# check memory
lsmem
# check CPUs
lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('
# start tests
python3 solution.py
```

### Docker commands

```bash
docker compose down
docker image rm neo4j:latest
```

### Links

- Instalation: http://neo4j.com/download/
- Online http://neo4j.com/sandbox/
- Reads
  - http://neo4j.com/developer/get-started/
  - http://neo4j.com/developer/cypher/
  - http://neo4j.com/developer/data-modeling/
  - http://neo4j.com/developer/guide-data-visualization/

