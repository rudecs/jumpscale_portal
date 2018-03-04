from JumpScale import j
from JumpScale.portal.portal.auth import auth
from JumpScale.portal.portal import exceptions
import json


class system_agentcontroller(j.code.classGetBase()):

    def __init__(self):
        self.scl = j.clients.osis.getNamespace('system')
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
        timeout=600, wait=True, queue="", gid=None, errorreport=True, session=None, htmlFormat=False, **kwargs):
        """
        schedules jumpscripts for execution
        """
        args = args if args else dict()
        jumpscript = self.scl.jumpscript.searchOne({'name': name, 'organization': organization})
        if not jumpscript:
            raise exceptions.BadRequest("Clould not find JumpScript {}:{}".format(organization, name))
        jsroles = jumpscript['roles']
        if nid is None and role is None:
            raise exceptions.BadRequest("Need to specify a role or nid")
        if nid:
            for (activegid, activenid), roles in self.listActiveSessions().items():
                if activenid == nid:
                    break
            else:
                raise exceptions.BadRequest("Nid {} is not active".format(nid))
            if jsroles and not set(roles).intersection(set(jsroles)):
                raise exceptions.BadRequest("Node specified can not execute JumpScript roles don't match")
        elif jsroles and role not in jsroles:
            raise exceptions.BadRequest("Specified role does not match JumpScript roles")

        for arg, value in kwargs.items():
            if arg.startswith('args_'):
                args[arg.strip('args_')] = value
        if isinstance(args, basestring):
            args = json.loads(args)
        job = self.ac.executeJumpscript(organization, name, nid, role, args, all_,
             timeout, wait, queue, gid, errorreport, session)
        if htmlFormat:
            job_url = 'click here to go to <a href="grid/job?id={}">job-{}</a>'.format(job['guid'], job['id'])
            return job_url
        return job

    @auth(['admin'])
    def loadJumpscripts(self, path, **kwargs):
        self.ac.loadJumpscripts(path)
