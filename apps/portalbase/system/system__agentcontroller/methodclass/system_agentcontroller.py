from JumpScale import j
from JumpScale.portal.portal.auth import auth
from JumpScale.portal.portal import exceptions
import json


class system_agentcontroller(j.code.classGetBase()):

    def __init__(self):
        self.ac = j.clients.agentcontroller.get()

    @auth(['admin'])
    def listActiveSessions(self, *args, **kwargs):

        sessions = self.ac.listActiveSessions()
        return sessions

    @auth(['admin'])
    def listSessions(self, *args, **kwargs):
        sessions = self.ac.listSessions()
        return sessions

    @auth(['admin'])
    def executeJumpscript(self, organization, name, nid=None, role=None, args={},all_=False,
        timeout=600,wait=True,queue="", gid=None, errorreport=True, session=None, **kwargs):
        if nid is None and role is None:
            raise exceptions.BadRequest("Need to specify a role or nid")
        if isinstance(args, basestring):
            args = json.loads(args)
        msg = self.ac.executeJumpscript(organization, name, nid, role, args, all_,
             timeout, wait, queue, gid, errorreport, session)
        return msg

    @auth(['admin'])
    def loadJumpscripts(self, path, **kwargs):
        self.ac.loadJumpscripts(path)
