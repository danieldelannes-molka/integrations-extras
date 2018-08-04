# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import pytest
import subprocess
import os
import time

from datadog_checks.apache_hive import apache_hive
from datadog_checks.errors import CheckException
from datadog_checks.utils.common import get_docker_hostname

def test_check(aggregator):
    c = apache_hive('apache_hive', {}, {}, None)

    instance={}

    with pytest.raises(CheckException):
      c.check(instance)

    with pytest.raises(CheckException):
      c.check({'ambari_api_url': 'localhost:6188'})

    with pytest.raises(CheckException):
      c.check({'APPID': 'hiveserver2'})
    
    c.check({'ambari_api_url': 'localhost:6188','APPID': 'hiveserver2','tags': {'key1':'value1'}})

    c.check({'ambari_api_url': 'localhost:6188','APPID': 'hiveserver2','hostname':'myhost'})

    c.check({'ambari_api_url': 'localhost:6188','APPID': 'hiveserver2','device_name':'mydevice'})

    c.check({'ambari_api_url': 'localhost:6188','APPID': 'hiveserver2'})

@pytest.mark.integration
def test_service_check(aggregator):
    c = apache_hive('apache_hive', {}, {}, None)

    HERE = os.path.dirname(os.path.abspath(__file__))
    args = [
        "docker-compose",
        "-f", os.path.join(HERE, 'docker-compose.yml')
    ]

    # start the Nginx container
    subprocess.check_call(args + ["up", "-d"])
    time.sleep(5)  # we should implement a better wait strategy :)

    # the check should send OK
    instance = {
        'ambari_api_url': 'localhost:6188'.format(get_docker_hostname()),
        'APPID': "hiveserver2"
    }
    c.check(instance)
    aggregator.assert_service_check('apache_hive.all_good', apache_hive.OK)

    # the check should send WARNING
    instance['APPID'] = "hiveserver2"
    c.check(instance)
    aggregator.assert_service_check('apache_hive.all_good', apache_hive.WARNING)

    # stop the container
    subprocess.check_call(args + ["down"])

    # the check should send CRITICAL
    c.check(instance)
    aggregator.assert_service_check('apache_hive.all_good', apache_hive.CRITICAL)
