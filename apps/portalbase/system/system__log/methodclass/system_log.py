from JumpScale import j
from JumpScale.portal.portal.auth import auth

class system_log(j.code.classGetBase()):

    """
     logs handling
    
    """

    def __init__(self):

        self._te = {}
        self.actorname = "log"
        self.appname = "system"
        self.scl = j.clients.osis.getNamespace('system', j.core.portal.active.osis)


    @auth(['level1', 'level2', 'level3'])
    def purge(self, age, **kwargs):
        start = int(j.base.time.getEpochAgo(age))
        query = {'epoch':{'$lt':start}}
        result = self.scl.log.deleteSearch(query)
        return result





