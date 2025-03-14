## MongoDB Data Modeling

### Prepare environment

Install `docker` and `mongosh`

```bash
docker compose up -d
```

### Test

```bash
mongosh "mongodb://user@localhost:27017/" -u user
```

### Docker commands

```bash
docker compose down
docker image rm mongodb-community-server:latest
```

### Links

- [Install MongoDB Community with Docker](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/#std-label-docker-mongodb-community-install)

  
