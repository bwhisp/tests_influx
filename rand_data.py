#!/usr/bin/python
# -*-coding:utf-8 -*-
import sys
import time

from random import randrange
from influxdb import InfluxDBClient

def build_data(value):
    return [
        {
            "measurement" : "response_time",
            "fields": {
                "value": value
            }
        }
    ]

def main(interval = 1, ip = "127.0.0.1"):
    """
    Cette fonction va s'occuper d'enregistrer une valeur aléatoire comprise entre 1 et 15
    à un intervalle de temps constant, par défaut 1s, dans une base de données InfluxDB
    dont on aura spécifié l'adresse IP si elle n'est pas en localhost.
    """
    # Connection à la base de données
    client = InfluxDBClient(ip, 8086, u'root', u'root','rand_data')
    while True:
        value = randrange(1,15)
	before = time.time()
        client.write_points(build_data(value))
	print("Time : "+str((time.time() - before)*1000))
        time.sleep(interval)



# On verifie le nombre d'argement et on execute le main avec les paramètres correspondants
if len(sys.argv) == 1:
    print(u"Usage : rand_data.py [-interval] [database's IP]")
    sys.exit(1)
elif len(sys.argv) == 2:
    arg = sys.argv[1]
    if arg[1] is "-":
        main(interval = int(arg[1:]))
    else:
        main(ip = arg)
else:
    # On a nos 2 arguments let's do this
    arg = sys.argv[1]
    main(int(arg[1:]), sys.argv[2])
