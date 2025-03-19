## MongoDB Data Modeling

### Preparing environment

Install `docker` and `mongosh`

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

### Replication test

Try executing `docker compose down` and `up` until the primary node is `mongo1` (27017). Because `replication_test.sh` works correctly only in that variant.

```bash
# start logging
script typescript_1
# start tests
bash -v replication_test.sh
```

### Performance analysis and integrity checking

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
docker image rm mongodb-community-server:latest
sudo rm -rf ${PWD}/rs_keyfile # need 'sudo' - execute a command as root
```

### Links

- [Install MongoDB Community with Docker](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/#std-label-docker-mongodb-community-install)

- [MongoDB Replica Set with Docker-compose](https://medium.com/@JosephOjo/mongodb-replica-set-with-docker-compose-5ab95c02af0d)

- [Mongo Local ReplicaSet setup using Docker](https://www.mongodb.com/community/forums/t/mongo-local-replicaset-setup-using-docker/300855)

