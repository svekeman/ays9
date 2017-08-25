# AYS Configuration

AYS is configured through a simple configuration file: `/optvar/cfg/jumpscale9.toml`.

AYS uses Redis to store its data, we need to be able to configure the connection to this database.

For Redis two modes are supported: `TCP` and `Unix socket`.

TCP example:
```toml
[redis]
addr = "localhost"
port = 6379
```

Unix socket example:
```yaml
redis:
  unixsocket: /tmp/redis.sock
```

If Redis configuration is provided the default behavior is to try to connect to JS redis over a unix socket located at `/tmp/redis.sock`.


## Redis server configuration

By default Redis is an in-memory only key-value store. But for our use case we want the data to be persisted on disk even after the server has stopped. To do that, we need to configure the Redis server to save its data on disk.

Here is an example of valid redis configuration for AYS:
```
# disable listening on tcp socket
port 0

# specify location of the unixsocket
unixsocket /tmp/ays.sock

# change location where to dump the database files
dir /optvar/data/redis-server

# By default Redis asynchronously dumps the dataset on disk. This mode is
# good enough in many applications, but an issue with the Redis process or
# a power outage may result into a few minutes of writes lost (depending on
# the configured save points).
#
# The Append Only File is an alternative persistence mode that provides
# much better durability. For instance using the default data fsync policy
# (see later in the config file) Redis can lose just one second of writes in a
# dramatic event like a server power outage, or a single write if something
# wrong with the Redis process itself happens, but the operating system is
# still running correctly.
#
# AOF and RDB persistence can be enabled at the same time without problems.
# If the AOF is enabled on startup Redis will load the AOF, that is the file
# with the better durability guarantees.
#
# Please check http://redis.io/topics/persistence for more information.
appendonly yes
```
