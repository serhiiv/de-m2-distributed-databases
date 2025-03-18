# Replica Set Elections

# view primary node
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'rs.hello()' | grep primary


# create collection items
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'use("task6"); db.items.drop(); db.createCollection("items");'


# Try to write with one node down and write concern level 3 
# and infinite timeout. Try to turn on the down node during the timeout.
# docker ps

# disconnect the secondary node - mongo2
docker network disconnect mongoCluster mongo2


# view work nodes
docker ps


# after 20 seconds, connect the secondary node - mongo 2
(sleep 20 && docker network connect mongoCluster mongo2) &


# add item ThinkPad X1 
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'use("task6"); db.items.insertOne({"model": "ThinkPad X1" }, { writeConcern: { w: 3, wtimeout: 0 } });'


# Like the previous point, set a finite timeout and wait for it to expire.
# Then, check if the data has been written and is available 
# for reading with the readConcern level majority.

# disconnect secondary node - mongo2
docker network disconnect mongoCluster mongo2


# view work nodes
docker ps


# add item ThinkPad X2
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'use("task6"); db.items.insertOne({ "model": "ThinkPad X2" }, { writeConcern: { w: 3, wtimeout: 5000 } });'


# reading data with the readConcern level majority
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'use("task6"); db.items.find({}).readConcern("majority");'


# connect secondary node - mongo2
docker network connect mongoCluster mongo2


# Disable the current primary node and demonstrate the primary node re-election.
# After the old primary node is back up, demonstrate 
# that new data that appeared during its downtime is being replicated.

# disconnect the primary node - mongo1
docker network disconnect mongoCluster mongo1


# view work nodes
docker ps


# wait election
sleep 20


# view primary node
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'rs.hello()' | grep primary


# add item ThinkPad X3
mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --eval \
'use("task6"); db.items.insertOne({ "model": "ThinkPad X3" });'


# connect the primary node - mongo1
docker network connect mongoCluster mongo1


# view work nodes
docker ps


# wait replication
sleep 2


# check replicated data
mongosh "mongodb://localhost:27017/" --eval \
'use("task6"); db.items.find({});'
