# Sandbox tips

## Kill all containers

docker container kill $(docker container ls -q)

## Download sandbox

- git clone https://github.com/algorand/sandbox

## Start sandbox

``` shell
cd sandbox
./sandbox up
```

## Map project into the sandbox

Add this project folder as bind volume in sandbox docker-compose.yml under key services.algod

``` .yaml
volumes:
  - type: bind
    source: <path> source: <path> ie: <path> could be ../algo_contracts_project
    target: /data
```

## Enter the sandbox

``` shell
cd sandbox
./sandbox enter algod
```
