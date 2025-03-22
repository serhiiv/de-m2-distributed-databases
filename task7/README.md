## Cassandra Data Modeling

### Preparing environment

Install `docker`

```bash
docker compose up -d
sleep 300
```

Use nodetool for check the status in all 3 nodes

```bash
docker exec cassandra-3 nodetool status
```

### Solution

```bash
script -c "bash -v solution.sh"
less typescript
```

### Cleaning environment

```bash
docker compose down
docker image rm cassandra:latest
```

### Links

- [Deploying Apache Cassandra Cluster (3 Nodes) with Docker Compose](https://medium.com/@kayvan.sol2/deploying-apache-cassandra-cluster-3-nodes-with-docker-compose-3634ef8345e8)
