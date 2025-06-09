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