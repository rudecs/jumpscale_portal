from JumpScale import j
import JumpScale.baselib.redisworker

class system_gitlab(j.code.classGetBase()):

    """
    Gitlab SYstem actors
    
    """

    def updateUserSpaces(self, username, **args):
         # Start cloning repos may be Async using actor call or something
        js = j.clients.redisworker.getJumpscriptFromName('jumpscale', 'clonegitlabspaces')
        job = j.clients.redisworker.execJumpscript(js.id, js, _sync=False, username=username)
        return job.id
    
    def checkUpdateUserSpaceJob(self, jobid):
        job = j.clients.redisworker.getJob(jobid)
        return job['state']