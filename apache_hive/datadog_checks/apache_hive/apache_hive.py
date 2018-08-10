# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

#gets the appid and ambari_api_url from the config file(also get the hostname, devic_name and tags if configured). It then uses the ambari_api_url to request the ambari metric api for a list of all ambari metrics. It then uses the appid to only record the metrics relating to hive. then it uses another ambari metic api call on each hive metric to get that metrics value at the time of request
import requests
import json

from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException
from hashlib import md5

class apache_hive(AgentCheck):
    hive_metrics={}
    #sends the check
    def check(self, instance):
        APPID=instance.get('APPID')
        ambari_api_url=instance.get('ambari_api_url')
        tags=instance.get('tags')
        hostname=instance.get('hostname')
        device_name=instance.get('device_name')
        if not APPID or not ambari_api_url:
           raise CheckException("Configuration error, please fix apache_hive.yaml")
        self.getListOfHiveMetrics(ambari_api_url)
        for key,value in self.hive_metrics.iteritems():
          data=self.getMetric(ambari_api_url,key,APPID)
          if data!=None:
            metricName='hive.'+key
            if value=='GAUGE':
                self.gauge(metricName, data, tags=tags, hostname=hostname, device_name=device_name)
            else:
                self.count(metricName, data, tags=tags, hostname=hostname, device_name=device_name)
        pass
    # makes an ambari metric api request for a list of all ambari metrics 
    def getListOfHiveMetrics(self,url):
        data=self.httpRequest('http://'+url+'/ws/v1/timeline/metrics/metadata')
        for metrics in data['hiveserver2']:
           self.hive_metrics[metrics['metricname']] = metrics['type']
    # makes an ambari metric api request for the value of a specific metric
    def getMetric(self, url,metricname, APPID):
        data=self.httpRequest('http://'+url+'/ws/v1/timeline/metrics?metricNames='+metricname+'&appId='+APPID)
        metrics = data['metrics']
        if metrics:
          timestamp = metrics[0]['starttime']
          return metrics[0]['metrics'][str(timestamp)]
        else:
          self.log.info('apache_hive '+metricname+' is empty!')
          return None
    #creates an http request
    def httpRequest(self,url):
       aggregation_key = md5(url).hexdigest()
       try:
         r = requests.get(url, timeout=8)
       except requests.exceptions.Timeout as e:
         self.timeout_event(url, 8, aggregation_key)
         return
       if r.status_code != 200:
         self.status_code_event(url, r, aggregation_key)
         return
       else:
         return r.json()
    # creates an event if the http request fails
    def timeout_event(self, url, timeout, aggregation_key):
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'http_check',
            'msg_title': 'URL timeout',
            'msg_text': '%s timed out after %s seconds.' % (url, timeout),
            'aggregation_key': aggregation_key
        })
    # creates an event if the http request does not return 200
    def status_code_event(self, url, r, aggregation_key):
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'http_check',
            'msg_title': 'Invalid response code for %s' % url,
            'msg_text': '%s returned a status of %s' % (url, r.status_code),
            'aggregation_key': aggregation_key
        })
