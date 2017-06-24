#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for
from redis import Redis

import os
import time
import sys

## Start time
start_time = time.time()

app= Flask (__name__)


message = os.environ.get ('MESSAGE', '(no message)') # ¯\_(ツ)_/¯
startupTime = os.environ.get ('STARTUP_TIME', 5) # No of seconds after startup that the /ready endpoint starts sending HTTP 200

redis_host = os.environ.get('REDIS_DB_SERVICE_HOST', 'localhost')
redis_port = os.environ.get('REDIS_DB_SERVICE_PORT', 6379)
redis = Redis (host=redis_host, port=redis_port)

configFile = "<ERR>"
try:
    f = open ("/etc/hello-world/hello.config", "r")
    configFile = f.read()
    pass
except Exception as e:
    configFile = e
    pass


instance_hits = 0
healthy_instance = True
ready_instance = True





def infinite_loop():
    """ Stallls execution by entering an infinite loop...
    """
    while True:
        time.sleep(5)


@app.route('/')
def home():
    """
    """
    global instance_hits
    global healthy_instance
    global message
    global configFile

    if (healthy_instance):
        redis.incr('hits') # Global counter in redis DB service
        instance_hits = instance_hits + 1 # local counter of this particular instance


        return render_template ('index.html', configFile=configFile, message=message, hostname=os.environ.get('HOSTNAME','(?)'),env=sorted(os.environ.items()), instance_hits=instance_hits,global_hits=redis.get('hits'), timeAlive=(time.time() - start_time))
#        return '{}. \n This Service (or "App") has served {} request(s), as recorded using the Redis database service found on {}:{}\n. \
#            This exact container instance is running for {} seconds and has so far served {} request(s) to this page.\n\n {}' \
#            .format(message, redis.get('hits'), redis_host, redis_port, (time.time() - start_time), instance_hits, os.environ)
    else:
        infinite_loop()



@app.route('/freeze')
def freeze():
    """ Freezes this instance by trapping future requests
    """
    global healthy_instance
    healthy_instance = False
    return render_template ('freeze.html'), 200
    #return "OK, instance will freeze (e.g. timeout) on future requests to homepage / probe endpoints", 200


@app.route('/kill')
def kill():
    """ kills this instance, immediately
    """
    try:
        sys.exit (123)
        pass
    except Exception as e:
        raise
    finally:
        return render_template ('kill.html'), 200
        pass


@app.route('/health')
def healthcheck():
    """ Answers healthcheck or provokes timeout when unhealty instance
    """
    global healthy_instance
    if (healthy_instance):
        return render_template ('health.html'), 200
        #return "Health OK", 200
    else:
        infinite_loop()


def instance_ready():
    """ Returns true iff ´startupTime´ seconds have been passed since startup
    """
    global start_time
    global startupTime
    return (time.time() - start_time) >= startupTime


@app.route('/ready')
def readinesscheck():
    """ If healthy and ready (e.g. startup time has already passed), return 200
    """
    global healthy_instance
    if (healthy_instance):
      if instance_ready():
        #return "Readiness OK", 200
        return render_template ('ready.html', message='We are ready now...'), 200
      else:
        #return "Not Ready, yet", 503
        return render_template ('ready.html', message='Sorry, not yet ready'), 503
    else:
        infinite_loop()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)
