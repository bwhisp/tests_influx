#!/usr/bin/python
# -*-coding:utf-8 -*-
from time import sleep
from random import randint

from influxdb import InfluxDBClient


tests = [{
	'name': 'CashIn',
	'id': 125,
	'actions': [
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'SMS','sim':'0609858343','probe':136 },
	],
	'operator':63,
	'product': 10
},{
	'name': 'Topup',
	'id': 126,
	'actions': [
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'USSD','sim':'0609858343','probe':136 },
		{'type':'SMS','sim':'0609858343','probe':136 },
	],
	'operator':63,
	'product': 10
}]


def build_data(type_data, action, infos, flag):
	"""
	This functions generate the JSON that will be sent to the database. It takes in entries the type of the data (str), the action, 
	the infos from the test instance and a flag (str) telling wether the USSD action is the first or the last in a row (or neither)
	"""
	tags = {
		"operator" : str(infos['operator']),
		"product" : str(infos['product']),
		"test" : str(infos['id']),
		"host" : str(action['probe']),
		"sim" : str(action['sim'])
	}

	if type_data.upper() == 'USSD':
		measurement = 'rt_ussd_screen'
		tags["screen_number"] = str(action["screen_number"])
		if type(flag) == str:
			tags['screen'] = flag
		value = randint(1,10)
	elif type_data.upper() == 'SMS':
		measurement = 'rt_sms_notifications'
		value = randint(15,40)
	else : 
		# C'est le rapport de test
		measurement = 'test_report'
		rate = randint(1,10)
		tags['status'] = 'Failed' if rate > 8 else 'Success'
		value = 1

	return {
		"measurement": measurement,
		"tags": tags,
		"fields": {
			"value" : value
		}
	}


def send_data(action, infos, flag):
	"""
	This function takes an action (JSON), basic infos from the test instance 
	and a flag (str), in the case of a USSD action, telling wether this is the first or the last USSD action in a row, or neither.
	After having processed the associated metric, it sends it to the database.
	"""
	client = InfluxDBClient(u'178.62.125.228',8086,u'root',u'root',u'metrics_data')
	metric = [build_data(action['type'], action, infos, flag)]
	client.write_points(metric)

def send_report(infos, host, sim):
	"""
	This function takes basic infos from the test instance, the host (str) and the sim number (str).
	After having processed the metric associated to the test report, it stores it into the database
	"""
	client = InfluxDBClient(u'178.62.125.228',8086,u'root',u'root',u'metrics_data')
	action = {
		'probe' : host,
		'sim' : sim
	}
	metric = [build_data('report',action, infos, None)]
	client.write_points(metric)


def main(tests):
	"""
	This function takes a list of tests as an entry and processes them so that their associated metrics are stored into the database.
	Once all the metrics have been sent to the database, a test report will be generated and stored into the database.
	"""
	while True: 
		n_tests = n_metrics = 0
		for test in tests:
			first_ussd = []
			last_ussd = []
			infos = {
				"name" : test["name"],
				"id" : test["id"],
				"operator" : test["operator"],
				"product" : test["product"]
			}
			count = 0

			for index, action in enumerate(test['actions']):
				if action['type']:
					count += 1
					action["screen_number"] = count
					if index == 0:
						send_data(action, infos,'first')
						host = str(action['probe']) 
						sim = str(action['sim'])
					elif index == len(test['actions']) - 1:
						send_data(action, infos,'last')
					elif test['actions'][index - 1]['type'] == 'SMS':
						send_data(action, infos,'first')
					elif test['actions'][index + 1]['type'] == 'SMS':
						send_data(action, infos,'last')
					else:
						send_data(action, infos, None)
				else: 
					send_data(action, infos, None)
				n_metrics += 1
				sleep(1)
			
			send_report(infos, host, sim)
			n_tests += 1
			print(u'Done : Test n°{}  >>> Total metrics sent : {}'.format(n_tests,n_metrics))
			sleep(1)

main(tests)