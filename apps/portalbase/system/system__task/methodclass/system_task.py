from JumpScale import j
from JumpScale.portal.portal import exceptions
import json


class system_task(object):
    def __init__(self):
        self.redis = j.clients.redis.getByInstance('system')
        self.rest = j.core.portal.active.rest

    def get(self, taskguid, **kwargs):
        task = self.redis.get('tasks.{}'.format(taskguid))
        greenlet = self.rest.tasks.get(taskguid)
        if task is None and greenlet is None:
            raise exceptions.NotFound("Task is not found")
        elif task is None and greenlet is not None:
            raise exceptions.BaseError(202, [], '')
        elif task is not None:
            return json.loads(task)

    def kill(self, taskguid, **kwargs):
        greenlet = self.rest.tasks.get(taskguid)
        if greenlet is None:
            raise exceptions.NotFound("Task is not found or not active")
        return greenlet.kill()
