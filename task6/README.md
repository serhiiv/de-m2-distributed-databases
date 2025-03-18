## MongoDB Data Modeling

### Preparing environment

Install `docker` and `mongosh`

Initializing the Replica Set:

```bash
bash generate_authentication_key.sh # need 'sudo' - execute a command as root
docker-compose up -d
```

Check Replica Set config

```bash
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval 'rs.hello()'
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval 'rs.config()'
```

### Replication test

Try executing "docker compose" down and up until the primary node is `mongo1` (27017). Because `replication_test.sh` works correctly only in that variant.

```bash
bash -v replication_test.sh
```

### Performance analysis and integrity checking



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

