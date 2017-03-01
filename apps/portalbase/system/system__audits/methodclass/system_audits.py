from JumpScale import j
from JumpScale.portal.portal.auth import auth


class system_audits(object):

    """
    System Audits

    """

    def __init__(self):
        self.scl = j.clients.osis.getNamespace('system', j.core.portal.active.osis)

    @auth(['level1'])
    def listAudits(self, username=None, responsetime=None, restcall=None, epoch=None, statuscode=None, page=None, size=None, **kwargs):
        """
        @param username str: username
        @param responsetime int: response time in milliseconds. (will get values greater than responsetime specified.)
        @param restcall str: rest endpoint api/method (i.e) /restmachine/cloudbroker/machine/start you should use (machine/start)
        @param epoch int: Epoch of the audit call timestamp
        @param statuscode int: status code returned
        @param page int: page number.
        @param size int: page size. (Note: None asks for all values.)

        result:int

        """
        if page is None:
            page = 0
        osissearch = {}
        if username is not None:
            osissearch['user'] = username
        if responsetime is not None:
            osissearch['responsetime'] = {'$gte': responsetime}
        if restcall is not None:
            osissearch['call'] = {'$regex': '.*%s.*' % restcall, '$options': 'i'}
        if epoch is not None:
            osissearch['timestamp'] = {'$gt': epoch}
        if statuscode is not None:
            osissearch['statuscode'] = statuscode

        res = self.scl.audit.search(osissearch, start=page, size=size)
        return res[1:]
