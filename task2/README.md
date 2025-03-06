https://gamov.io/posts/2017/06/08/how-to-scale-hazelcast-docker-containers-with-docker-compose.html

https://github.com/hazelcast/hazelcast-code-samples/blob/master/hazelcast-integration/docker-compose/00_vanilla/docker-compose.yml

docker compose up -d
docker compose down


docker run \
    -it \
    --network hazelcast-network \
    --rm \
    -e HZ_NETWORK_PUBLICADDRESS=127.0.0.1:5701 \
    -e HZ_CLUSTERNAME=dev \
    -p 5701:5701 hazelcast/hazelcast:5.4.0