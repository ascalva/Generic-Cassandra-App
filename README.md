## Flask Application Using Apache Cassandra ##

### Setup ###
Starting the cluster of Cassandra nodes and Flask server can be done using the docker compose command (Cassandra nodes take about a minute to spin up.):

```
docker-compose -f docker-compose.yaml up --build
```

Connecting to a Cassandra node from cqlsh can be done using the following docker command:

```
docker run -it --network cas-net --rm cassandra cqlsh <cassandra-container-name>
```

