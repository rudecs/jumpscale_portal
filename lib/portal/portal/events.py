from JumpScale import j
from JumpScale.portal.portal import exceptions
import gevent
import json


EVENTKEY = 'events.events'
SESSIONKEY = 'events.session.'

class EventSubScriber(object):
    def __init__(self, redis):
        self.redis = redis
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(EVENTKEY)
        self.pubsub.ignore_subscribe_messages = True

    def start(self):
        gevent.spawn(self.run)

    def run(self):
        for event in self.pubsub.listen():
            for key in self.redis.keys(SESSIONKEY + '*'):
                self.redis.getQueue(key).put(event['data'])


class Events(object):
    GETS = {}

    def __init__(self, session, redis, ctx):
        self.ctx = ctx
        self.session = session
        self.redis = redis

    def get(self, key):
        queuename = SESSIONKEY + key
        self.redis.set(queuename, 1, ex=60)

        def get():
            queue = self.redis.getQueue(queuename)
            data = queue.get(timeout=30)
            if data:
                return json.loads(data)
            return 0
        puller = self.GETS.get(queuename)
        if puller:
            del Events.GETS[queuename]
            puller.kill()
        greenlet = gevent.spawn(get)
        Events.GETS[queuename] = greenlet
        greenlet.join()
        if greenlet.value is None:
            return
        Events.GETS.pop(queuename, None)
        return greenlet.value or None

    def sendMessage(self, title, text, level='info', **kwargs):
        msg = {'eventtype': 'message', 'title': title, 'text': text, 'type': level}
        if kwargs:
            msg.update(kwargs)
        self.sendEvent(msg)

    def sendEvent(self, event):
        self.redis.publish(EVENTKEY, json.dumps(event))

    def runAsync(self, func, args, kwargs, title, success, error):
        def runner():
            try:
                func(*args, **kwargs)
            except (Exception, exceptions.BaseError),  e:
                eco = j.errorconditionhandler.processPythonExceptionObject(e)
                errormsg = error + "</br> For more info check <a href='/grid/error condition?id=%s'>error</a> details" % eco.guid
                self.sendMessage(title, errormsg, 'error', hide=False)
                return
            refreshhint = self.ctx.env.get('HTTP_REFERER')
            self.sendMessage(title, success, 'success', refresh_hint=refreshhint)
        self.sendMessage(title, 'Started')
        gevent.spawn(runner)

    def waitForJob(self, job, success, error, title=None):
        gevent.spawn(self._waitForJob, job, success, error, title)

    def _waitForJob(self, job, success, error, title):
        title = title or 'Job Info'
        acl = j.clients.agentcontroller.get()
        job = acl.waitJumpscript(job=job)
        if job['state'] != 'OK':
            error += "</br> For more info check <a href='/grid/job?id=%(guid)s'>job</a> details" % job
            self.sendMessage(title, error, 'error', hide=False)
        else:
            refreshhint = self.ctx.env.get('HTTP_REFERER')
            self.sendMessage(title, success, 'success', refresh_hint=refreshhint)
