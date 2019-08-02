# Redis

[Redis home](https://redis.io/)

## docker

``` bash
docker run -d  -p 6380:6379 redis --requirepass '123456'
```

``` bash
docker exec -it [container_id] redis-cli -h [host] -p [port] -a [password]

# eg.
docker exec -it 05f92d468e05 redis-cli -a 123456
```
