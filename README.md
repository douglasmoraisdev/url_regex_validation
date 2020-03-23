# Url Regex Validator

A microservice for url validation based on regex whitelist. This python microservice receive and validate regex and urls via RabbitMq Queues, and persists on Mysql Databases. A Docker-compose file is used for orquestration.

# Running service

> $ docker-compose up

# Running unit tests
Using Docker
> $ docker exec -it <runing_container_name> python -m unittest

Standalone service
> $ python -m unittest

# Configuration

Use these files for configuration:

When running with docker-compose (default)
> src/.docker.env

When running only the microservice (external Mysql and/or Rabbitmq)
> src/.env

To configure automated tests env variables
> src/tests/.env

# Inserting new regex on Whitelist
Post this payload on RabbitMQ. Queue: $INSERTION_QUEUE (.env):

```json
{"client": <string/nullable>, "regex": <string>}
```
```client```
A client name (string), if 'null', will be saved on 'global' whitelist

```regex```
A url format regex for whitelist

# Validating Urls
Post this payload on RabbitMQ. Queue: $VALIDATION_QUEUE (.env):


```json
{"client": <string>, "url": <string>, "correlationId": <integer>}
```
```client:```
A client name (string), if 'null', will be match on 'global' whitelist

```url:```
A url for validation

```correlationId:```
A UUID for relation queries and responses

# Validating results (Response)

This payload will be post on RabbitMQ response routing key ($RESPONSE_ROUTING_KEY), when a validating occured.

```json
{"match": <boolean>, "regex": <string/nullable>, "correlationId": <integer>}
```

```match:```
Result of whitelist validation: true or false

```regex:```
The matched regex. If no match found will be 'null'

```correlationId:```
The correlationId origin of validation