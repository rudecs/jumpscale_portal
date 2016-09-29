from JumpScale import j
from JumpScale.portal.portal import exceptions
import json


class system_task(object):
    def __init__(self):
        self.redis = j.clients.redis.getByInstance('system')
        self.ws = j.core.portal.active.ws

    def get(self, taskguid, **kwargs):
        task = self.redis.get('task.{}'.format(taskguid))
        greenlet = self.ws.tasks.get(taskguid)
        if task is None and greenlet is None:
            raise exceptions.NotFound("Task is not found")
        elif task is None and greenlet is not None:
            raise exceptions.BaseError(202, [], '')
        elif task is not None:
            return json.loads(taskguid)

    def kill(self, taskguid, **kwargs):
        greenlet = self.ws.tasks.get(taskguid)
        if greenlet is None:
            raise exceptions.NotFound("Task is not found or not active")
        return greenlet.kill()
