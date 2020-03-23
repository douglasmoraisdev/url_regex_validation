#!/usr/bin/env python3
from time import sleep
from models.connectors.mysqldb import MySQLDBConnection
from services.rabbitmq import RabbitmqService

mysql = MySQLDBConnection().migration_connection_from_dotenv()

while True:
    try:
        #wait for mysql connection
        mysql.connect()

    except Exception as e:
        print("Waiting Mysql... %s" % '')
        sleep(5)
        continue

    try:
        #wait for rabbitmq
        rabbitmq = RabbitmqService()

    except Exception as e:
        print("Waiting RabbitMq... %s" % '')
        sleep(5)
        continue

    break

print('Connected!')