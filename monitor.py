# =============================================================================
# monitor.py
#
# A class to help facilitate API calls to the 'monitor' service for WPM.
#
# Requires non-standard 'client' (WPM) python library to be installed.
#
# Version: 1.0
# Date: 02/15/13
# Author: Tyler Fullerton
# =============================================================================
from client import Client

class Monitor(Client):

	# -------------------------------------------------------------------------
	# Create a new Monitor object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	def __init__(self, key, secret):
		Client.__init__(self, key, secret, 'monitor', '', 'GET')

	# -------------------------------------------------------------------------
	# Override string representation of Monitor object.
	def __str__(self):
		return Client.__str__(self)

	# -------------------------------------------------------------------------
	# API interaction to create a monitor to the WPM platform.
	#
	# params - Dictionary containing the details of the monitor to create.
	def createMonitor(self, params):
		self.setService('monitor')
		self.setMethod('')
		self.setHttpMethod('POST')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to list monitors on the WPM platform.
	def listMonitors(self):
		self.setService('monitor')
		self.setMethod('')
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get a monitor from the WPM platform.
	#
	# monitorId - ID of the monitor to get.
	def getMonitor(self, monitorId):
		self.setService('monitor')
		self.setMethod(monitorId)
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to update a monitor on the WPM platform.
	#
	# monitorId - ID of the monitor to delete.
	# params - Dictionary containing the update details for the monitor.
	def updateMonitor(self, monitorId, params):
		self.setService('monitor')
		self.setMethod(monitorId)
		self.setHttpMethod('PUT')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to delete a monitor on the WPM platform.
	#
	# monitorId - ID of the monitor to delete.
	def deleteMonitor(self, monitorId):
		self.setService('monitor')
		self.setMethod(monitorId)
		self.setHttpMethod('DELETE')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get monitoring samples for a monitor.
	#
	# monitorId - ID of the monitoring service.
	# params - Dictionary that provides startDate and endDate values.
	def getMonitorSamples(self, monitorId, params):
		self.setService('monitor')
		self.setMethod(monitorId + '/sample')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get raw monitoring data for a sample.
	#
	# monitorId - ID of the monitoring service.
	# sampleId - ID of the particular sample to get raw data for.
	def getRawMonitorSample(self, monitorId, sampleId):
		self.setService('monitor')
		self.setMethod(monitorId + '/sample/' + sampleId)
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get aggregate monitoring data for a monitor.
	#
	# monitorId - ID of the monitoring service.
	# params - Dictionary that provides startDate, endDate & frequency values.
	def getAggregateMonitorData(self, monitorId, params):
		self.setService('monitor')
		self.setMethod(monitorId + '/aggregate')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get a monitoring summary for a monitor.
	#
	# monitorId - ID of the monitoring service.
	def getMonitorSummary(self, monitorId):
		self.setService('monitor')
		self.setMethod(monitorId + '/summary')
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to list monitoring locations on the WPM platform.	
	def getLocations(self):
		self.setService('monitor')
		self.setMethod('locations')
		self.setHttpMethod('GET')
		return self.call()
	
# -----------------------------------------------------------------------------
# Testing code
if __name__ == '__main__':

	import json
	import time
	import string
	import random

	# Variables for testing	
	key		= '[KEY]'
	secret	= '[SECRET]'

	# Create a random service name
	svcName	= ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))

	# Monitoring service parameters
	serviceParams = {
		'name'			: svcName,
		'description'	: 'This is a test service',
		'interval'		: 1,
		'testScript'	: 'default_script',
		'locations'		: 'washingtondc,sanjose,london',
	}

	# Dates for getting raw data
	now			= time.localtime()
	today		= time.strftime('%Y-%m-%d', now)
	dateParams	= {
		'startDate'	: today,
		'endDate'	: today,
	}

	# TODO: This service ID is for testing the API calls that get sample data.  
	# If you use the service that is created as part of the other tests you'll have to
	# include a rather long sleep (for a 1 minute monitoring a sleep of 4 minutes wasn't
	# sufficient).  I recommend setting up a service in your account that is always on for
	# testing purposes.  Then set the testService value to the monitor ID for that service.
	testService = '[EXISTING SERVICEID]'

	# Store service ID for testing
	serviceId 	= ''

	# Test __init__
	print '**** TEST: __init__'
	monitorClient = Monitor(key, secret)
	print monitorClient

	# Test __str__
	print '**** TEST: __str__'
	print monitorClient

	# Test createMonitor
	print '**** TEST: createMonitor'
	response	= monitorClient.createMonitor(serviceParams)
	jsonObj		= json.loads(response.text)
	serviceId	= jsonObj.get('data', {}).get('items', {}).get('id', '')
	print 'Created Service (id):', serviceId

	# Test getMonitor
	print '**** TEST: getMonitor'
	response	= monitorClient.getMonitor(serviceId)
	print response.text

	# Test updateMonitor
	print '**** TEST: updateMonitor'
	serviceParams['description'] = 'UPDATED DESCRIPTION!'
	response	= monitorClient.updateMonitor(serviceId, serviceParams)
	time.sleep(5)
	response	= monitorClient.getMonitor(serviceId)
	jsonObj		= json.loads(response.text)
	newDesc		= jsonObj.get('data', {}).get('items', [])[0].get('description', '')
	print 'Updated Description:', newDesc	

	# Test getMonitorSample
	print '**** TEST: getMonitorSamples'
	response	= monitorClient.getMonitorSamples(testService, dateParams)
	jsonObj		= json.loads(response.text)
	sampleId	= jsonObj.get('data', {}).get('items', [])[0].get('id', '')
	print 'Got a sample ID:', sampleId

	# Test getRawMonitorSample
	print '**** TEST: getRawMonitorSample'
	response	= monitorClient.getRawMonitorSample(testService, sampleId)
	print response.text

	# Test getAggregateMonitorData
	print '**** TEST: getAggregateMonitorData'
	dateParams['frequency'] = 'hour'
	response	= monitorClient.getAggregateMonitorData(testService, dateParams)
	print response.text
	
	print '**** TEST: getMonitorSummary'
	response	= monitorClient.getMonitorSummary(testService)
	print response.text

	# Test deleteMonitor
	print '**** TEST: deleteMonitor'
	response	= monitorClient.deleteMonitor(serviceId)
	print response.text

	# Test listMonitors
	print '**** TEST: listMonitors'
	response	= monitorClient.listMonitors()
	jsonObj		= json.loads(response.text)
	serviceList	= jsonObj.get('data', {}).get('items', [])
	print 'Got:',len(serviceList)
	
	# Test getLocations
	response	= monitorClient.getLocations()
	jsonObj		= json.loads(response.text)
	locList		= jsonObj.get('data', {}).get('items', [])
	print 'Got:',len(locList)
