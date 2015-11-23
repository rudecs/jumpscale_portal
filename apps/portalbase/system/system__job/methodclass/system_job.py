from JumpScale import j
from JumpScale.portal.portal.auth import auth

class system_job(j.code.classGetBase()):

    """
     jobs handling
    
    """

    def __init__(self):

        self._te = {}
        self.actorname = "job"
        self.appname = "system"
        self.scl = j.clients.osis.getNamespace('system', j.core.portal.active.osis)


    @auth(['level1', 'level2', 'level3'])
    def purge(self, age, **kwargs):
        start = int(j.base.time.getEpochAgo(age))
        query = {'timeStop':{'$lt':start}}
        result = self.scl.job.deleteSearch(query)
        return result