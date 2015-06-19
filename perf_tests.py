#!/usr/bin/python
# -*-coding:utf-8 -*-
import sys
import time

from influxdb import InfluxDBClient

client = InfluxDBClient(u'178.62.125.228', 8086, u'root', u'root','rand_data')

## 5 Secondes
b0 = time.time()
result = client.query('select mean(value) from response_time where time > now() - 2d group by time(5s);')
a0 = time.time()
print("Query grouped by 5s : ")
print("Time : "+ str((a0-b0)*1000) + " ms")
n = 0
for a in result.get_points():
	n += 1
print("Size : "+str(n)+" samples")
print("Size : "+str(sys.getsizeof(result.raw))+" octets\n")


## 10 Secondes
b0 = time.time()
result = client.query('select mean(value) from response_time where time > now() - 2d group by time(10s);')
a0 = time.time()
print("Query grouped by 10s : ")
print("Time : "+ str((a0-b0)*1000) + " ms")
n = 0
for a in result.get_points():
	n += 1
print("Size : "+str(n)+" samples")
print("Size : "+str(sys.getsizeof(result.raw))+" octets\n")

## 30 Secondes
b0 = time.time()
result = client.query('select mean(value) from response_time where time > now() - 2d group by time(30s);')
a0 = time.time()
print("Query grouped by 30s : ")
print("Time : "+ str((a0-b0)*1000) + " ms")
n = 0
for a in result.get_points():
	n += 1
print("Size : "+str(n)+" samples")
print("Size : "+str(sys.getsizeof(result.raw))+" octets\n")

## 1 minute
b0 = time.time()
result = client.query('select mean(value) from response_time where time > now() - 2d group by time(1m);')
a0 = time.time()
print("Query grouped by minute : ")
print("Time : "+ str((a0-b0)*1000) + " ms")
n = 0
for a in result.get_points():
	n += 1
print("Size : "+str(n)+" samples")
print("Size : "+str(sys.getsizeof(result.raw))+" octets\n")

## 2 minutes
b0 = time.time()
result = client.query('select mean(value) from response_time where time > now() - 2d group by time(2m);')
a0 = time.time()
print("Query grouped by 2 minutes : ")
print("Time : "+ str((a0-b0)*1000) + " ms")
n = 0
for a in result.get_points():
	n += 1
print("Size : "+str(n)+" samples")
print("Size : "+str(sys.getsizeof(result.raw))+" octets\n")


