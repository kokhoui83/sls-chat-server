# Serverless Chat Server (python)

## Requirements
- python 3.8
- serverless
- node 12

## Build
```
sls package
```

## Deployment
- ensure deployment machine has the required AWS creds
```
sls deploy
```

## Checked deployed lambda logs
```
sls logs -f <function>

# example
sls logs -f hello
```

## Cleanup deployment
```
sls remove
```