# zookeeper

- [zookeeper](#zookeeper)
  - [zookeeper systemd service file](#zookeeper-systemd-service-file)
  - [zookeeper on docker](#zookeeper-on-docker)
  - [ZooKeeper Commands: The Four Letter Words](#zookeeper-commands-the-four-letter-words)

[Home](http://zookeeper.apache.org/)

## zookeeper systemd service file

```bash
vim /lib/systemd/system/redis.service
```

```systemd
[Unit]
Description=zookeeper
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/zookeeper/bin/zkServer.sh start
ExecStop=/usr/local/zookeeper/bin/zkServer.sh stop
Restart=always

[Install]
WantedBy=multi-user.target
```

## zookeeper on docker

[Docker Image](https://hub.docker.com/_/zookeeper)

``` bash
vim stack.yml
```

``` yml
version: '3.1'

services:
  zoo1:
    image: zookeeper
    restart: always
    hostname: zoo1
    ports:
      - 2181:2181
    environment:
      ZOO_MY_ID: 1
      ZOO_SERVERS: server.1=0.0.0.0:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo2:
    image: zookeeper
    restart: always
    hostname: zoo2
    ports:
      - 2182:2181
    environment:
      ZOO_MY_ID: 2
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=0.0.0.0:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo3:
    image: zookeeper
    restart: always
    hostname: zoo3
    ports:
      - 2183:2181
    environment:
      ZOO_MY_ID: 3
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=0.0.0.0:2888:3888;2181
```

``` bash
docker stack deploy -c stack.yml zookeeper
```

## ZooKeeper Commands: The Four Letter Words

[ZooKeeper Commands: The Four Letter Words](http://zookeeper.apache.org/doc/r3.4.8/zookeeperAdmin.html#sc_zkCommands)

conf
> New in 3.3.0: Print details about serving configuration.

cons
> New in 3.3.0: List full connection/session details for all clients connected to this server. Includes information on numbers of packets received/sent, session id, operation latencies, last operation performed, etc...

crst
> New in 3.3.0: Reset connection/session statistics for all connections.

dump
> Lists the outstanding sessions and ephemeral nodes. This only works on the leader.

envi
> Print details about serving environment

ruok
> Tests if server is running in a non-error state. The server will respond with imok if it is running. Otherwise it will not respond at all.
> A response of "imok" does not necessarily indicate that the server has joined the quorum, just that the server process is active and bound to the specified client port. Use "stat" for details on state wrt quorum and client connection information.

srst
> Reset server statistics.

srvr
> New in 3.3.0: Lists full details for the server.

stat
> Lists brief details for the server and connected clients.

wchs
> New in 3.3.0: Lists brief information on watches for the server.

wchc
> New in 3.3.0: Lists detailed information on watches for the server, by session. This outputs a list of sessions(connections) with associated watches (paths). Note, depending on the number of watches this operation may be expensive (ie impact server performance), use it carefully.

wchp
> New in 3.3.0: Lists detailed information on watches for the server, by path. This outputs a list of paths (znodes) with associated sessions. Note, depending on the number of watches this operation may be expensive (ie impact server performance), use it carefully.

mntr
> New in 3.4.0: Outputs a list of variables that could be used for monitoring the health of the cluster.
