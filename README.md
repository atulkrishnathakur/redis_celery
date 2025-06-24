## This project we have created using fastapi framwork

## update your system

```
atul@atul-Lenovo-G570:~$ sudo apt update

```

## install the `redis-server`
1. The redis server will be install globaly. It will be not install in python virtual environment
```
atul@atul-Lenovo-G570:~$ sudo apt install redis-server

```

## check the redis cli by `redis-cli ping` command

```
atul@atul-Lenovo-G570:~$ redis-cli ping

```

1. If the output is `PONG`. It means redis has been installed successfully.


## check the system status for redis

```
atul@atul-Lenovo-G570:~$ sudo systemctl status redis

```

## Install the `redis` library of python
1. Go to your project directory and start the virual environment
```
atul@atul-Lenovo-G570:~/redis_celery$ source env/bin/activate

```

2. Install the redis client library for python. This command install `redis-py` python library.

```
(env) atul@atul-Lenovo-G570:~/redis_celery$ pip install redis

```

## How to see all redis keys that stored in redis database

```
(env) atul@atul-Lenovo-G570:~/redis_celery$ redis-cli keys '*'

```

## Shows the all keys and its expiration status

```
(env) atul@atul-Lenovo-G570:~/redis_celery$ redis-cli info keyspace
# Keyspace
db0:keys=1,expires=0,avg_ttl=0

```

## How to see specific key value

```
(env) atul@atul-Lenovo-G570:~/redis_celery$ redis-cli get loginuserdata
"{\"id\": 8, \"emp_name\": \"Atul\", \"email\": \"atul@yopmail.com\", \"status\": 1}"
(env) atul@atul-Lenovo-G570:~/redis_celery$ 

```


## How to set redis key with time

1. You can pass NX, EX, PX, and XX as keyword arguments in the set() method of redis-py. Here's how to use them with your self.redis_client.set(session_key, json_data) call:

```
self.redis_client.set(
    session_key,
    json_data,
    ex=900,       # Expire in 900 seconds (15 minutes)
    px=None,      # Or use px=900000 for milliseconds
    nx=True,      # Only set if key does NOT exist
    xx=False      # Don't require key to already exist
)

```

2. ex=seconds: Set expiration in seconds.
3. px=milliseconds: Set expiration in milliseconds (alternative to ex).
4. nx=True: Only set if the key does not exist.
5. xx=True: Only set if the key already exists.
6. You should only use one of nx=True or xx=True at a time—using both will cancel each other out.