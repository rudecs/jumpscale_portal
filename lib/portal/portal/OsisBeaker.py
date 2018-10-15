from JumpScale import j
from JumpScale.grid.serverbase.Exceptions import RemoteException
from beaker.container import NamespaceManager
import json


class OsisBeaker(NamespaceManager):

    def __init__(self, id, namespace_args, **kwargs):
        self._namespace = 'system'
        self._category = 'sessioncache'
        self.namespace = id
        self._client = namespace_args['client']
        self._rcl = j.clients.redis.getByInstance('system')
        self._redis_key = 'sessions:{}'.format(self.namespace)

    def _redis_set(self, key, value):
        try:
            dbvalue = self._redis_get(key)
            dbvalue.update(value)
            value = dbvalue
        except KeyError:
            pass
        self._rcl.set(self._redis_key, json.dumps(value), ex=600)

    def _redis_get(self, key):
        data = self._rcl.get(self._redis_key)
        if data is None:
            raise KeyError(key)
        return json.loads(data)

    def __getitem__(self, key):
        key = "%s_%s" % (self.namespace, key)
        if self._client.exists(categoryname=self._category, namespace=self._namespace, key=key):
            return self._client.get(categoryname=self._category, namespace=self._namespace, key=key)
        else:
            return self._redis_get(key)

    def __setitem__(self, key, value):
        nkey = "%s_%s" % (self.namespace, key)
        if 'user' not in value:
            self._remove(key)
            return
        elif value['user'] == 'guest':
            self._redis_set(key, value)
            return
        self._client.set(categoryname=self._category, namespace=self._namespace, key=nkey, value=value)

    def _remove(self, key):
        key = "%s_%s" % (self.namespace, key)
        try:
            self._client.delete(categoryname=self._category, namespace=self._namespace, key=key)
        except RemoteException as error:
            if error.eco.exceptionclassname == 'KeyError' or error.eco.category == 'osis.objectnotfound':
                return
            raise

    def __contains__(self, key):
        key = "%s_%s" % (self.namespace, key)
        return self._client.exists(self._namespace, self._category, key)

    def __delitem__(self, key, **kwargs):
        self._remove(key)

    def acquire_read_lock(self, **kwargs):
        return True

    def release_read_lock(self, **kwargs):
        return True

    def acquire_write_lock(self, **kwargs):
        return True

    def release_write_lock(self, **kwargs):
        return True
