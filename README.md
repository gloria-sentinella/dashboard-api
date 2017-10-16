# dashboard-api
dashboard-api

``` bash
$ docker build -t nuage-api .
$ docker run --name nuage-api -v $PWD/:/app/ -p 8000:8000 -d -i -t nuage-api:latest
$ docker exec -it nuage-api service supervisor restart
```