from bottle import route, run, request, get, post, response
from datetime import datetime
import codecs
from redis import Redis
from rq_scheduler import Scheduler
from rq.queue import FailedQueue

from datetime import timedelta

import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from restful_scheduler.action import request_url

@get('/scheduler') # or @route('/login')
def homepage():

    from datetime import datetime

    return '''
        <h2>restful scheduler </h2> version:{}
        <p>
           <a href="scheduler/list_todo">list todo task</a>,
           <a href="scheduler/log?limit=10">list last n log</a>
        </p>
        <form action="/scheduler/add" method="get">
            url: <input name="url" type="text" value="http://vbuluo.com/req-{}" size=80 />
            <br/>
            minutes_delta: <input name="minutes_delta" type="number" value="10"/>
            <br/>
            <input value="Add" type="submit" />
        </form>
    '''.format(
        "2015-04-03",
        datetime.now().isoformat().replace(":","-")
    )

filename_log = "/tmp/log.txt"

@get('/scheduler/add')
def add():
    #print str(request.query)

    url = request.query['url']
    minutes_delta = int(request.query['minutes_delta'])


    scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue

    # Schedule a job to run 10 minutes, 1 hour and 1 day later
    job = scheduler.enqueue_in(timedelta(minutes=minutes_delta), request_url, **{"url":url})

    msg = u'[{}][scheduler/add] {} scheduled after {} minutes. job id {}\n'.format(datetime.now().isoformat()[:19], url, minutes_delta, job.id)
    print msg

    with codecs.open(filename_log, "a", encoding="utf-8") as f:
        f.write(msg)

    return msg


@get('/scheduler/list_todo')
def list_todo():
    scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue

    response.content_type = 'text/plain; charset=utf-8'

    list_of_job_instances = scheduler.get_jobs()
    msg = "\n".join([ str(job) for job in list_of_job_instances])
    print msg

    return msg

@get('/scheduler/log')
def enqueue():
    limit = -1 * int(request.query.get('limit', 10)) #from last line

    response.content_type = 'text/plain; charset=utf-8'
    with codecs.open(filename_log, "r", encoding="utf-8") as f:
        return "".join(f.readlines()[limit:])

if __name__ == '__main__':
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("baidu.com",80))
    ipaddress = s.getsockname()[0]
    s.close()
    print ipaddress

    #run(host=ipaddress, port=8080)
    run(host='localhost', port=8080)