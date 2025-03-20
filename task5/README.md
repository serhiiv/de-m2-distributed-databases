## Cassandra Data Modeling

### Preparing environment

Install `docker`

Initializing the Replica Set:

Before launching the containers, you must generate a key and change the "initiate_replica_set.mongodb" file, specifying the current IP address of the docker host.

```bash
bash generate_authentication_key.sh # need 'sudo' - execute a command as root
nano initiate_replica_set.mongodb  # schange IP
docker-compose up -d
```

Check Replica Set configuration

```bash
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval 'rs.hello()'
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval 'rs.config()'
```

### #1 Replication test

Try executing `docker compose down` and `up` until the primary node is `mongo1` (27017). Because `replication_test.sh` works correctly only in that variant.

```bash
# start logging
script typescript_1
# start tests
bash -v replication_test.sh
```

### #2 Performance analysis and integrity checking

```bash
# start logging
script typescript_2
# check memory
lsmem
# check CPUs
lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('
# start tests
python3 solution.py
```

### Cleaning environment

```bash
docker compose down
docker image rm mongo:latest
sudo rm -rf ${PWD}/rs_keyfile # need 'sudo' - execute a command as root
```

### Links

- [Deploying Apache Cassandra Cluster (3 Nodes) with Docker Compose](https://medium.com/@kayvan.sol2/deploying-apache-cassandra-cluster-3-nodes-with-docker-compose-3634ef8345e8)
