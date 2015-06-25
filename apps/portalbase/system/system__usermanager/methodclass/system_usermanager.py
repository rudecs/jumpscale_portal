from JumpScale import j
from JumpScale.portal.portal.auth import auth

class system_usermanager(j.code.classGetBase()):

    """
    register a user (can be done by user itself, no existing key or login/passwd is needed)

    """

    def __init__(self):

        self._te = {}
        self.actorname = "usermanager"
        self.appname = "system"
        self.osiscl = j.core.portal.active.osis
        self.modelUser = j.clients.osis.getCategory(self.osiscl, 'system', 'user')

    def _authSelf(self,user,kwargs):
        ctx=kwargs["ctx"]
        if not user==ctx.env['beaker.session']["user"]:
            raise RuntimeError("Authentication Error")

    def authenticate(self, name, secret, **kwargs):
        """
        The function evaluates the provided username and password and returns a session key.
        The session key can be used for doing api requests. E.g this is the authkey parameter in every actor request.
        A session key is only vallid for a limited time.
        param:username username to validate
        param:password password to validate
        result str,,session
        """
        ctx = kwargs['ctx']
        if j.core.portal.active.auth.authenticate(name, secret):
            session = ctx.env['beaker.get_session']() #create new session
            session['user'] = name
            session.save()
            return session.id
        ctx.start_response('401 Unauthorized', [])
        return 'Unauthorized'

    def userget(self, name, **kwargs):
        """
        get a user
        param:name name of user
        """
        return self.modelUser.get("%s_%s"%(j.application.whoAmI.gid,name))

    def usergroupsget(self, user, **args):
        """
        return list of groups in which user is member of
        param:user name of user
        result list(str)

        """
        raise NotImplementedError("not implemented method getusergroups")
        usermanager = j.apps.system.usermanager
        user = self._userGet(user)

        if user == None:
            # did not find user
            result = []
        else:
            # print "usergroups:%s" % user.groups
            result = user.groups

        return result

    def _getUser(self, user):
        users = self.modelUser.search({'id': user})[1:]
        if not users:
            return None
        return self.modelUser.get(users[0]['guid'])

    @auth(['admin'])
    def setGroups(self, username, groups, **kwargs):
        ctx = kwargs['ctx']
        user = self._getUser(username)
        if not user:
            ctx.start_resonpnse('404 Not Found', [('Content-Type', 'text/plain')])
            return "User %s not found" % username
        if not isinstance(groups, list):
            ctx.start_resonpnse('400 Bad Request', [('Content-Type', 'text/plain')])
            return "Groups paramter should be a list"
        user.groups = groups
        self.modelUser.set(user)
        return True

    @auth(['admin'])
    def delete(self, username, **kwargs):
        user = self._getUser(username)
        if not user:
            return True
        self.modelUser.delete(user.guid)
        return True

    def groupcreate(self, name, groups, **args):
        """
        create a group
        param:name name of group
        param:groups comma separated list of groups this group belongs to
        result bool

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method groupcreate")

    def usercreate(self, name, passwd, key, groups, emails, userid, reference, remarks, config, **args):
        """
        create a user
        param:name name of user
        param:passwd passwd
        param:key specific key can be empty
        param:groups comma separated list of groups this user belongs to
        param:emails comma separated list of email addresses
        param:userid optional user id; leave 0 when not used; when entered will update existing record
        param:reference reference as used in other application using this API (optional)
        param:remarks free to be used field by client
        param:config free to be used field to store config information e.g. in json or xml format
        result bool

        """
        groups = groups.split(",")
        emails = emails.split(",")
        if userid == 0:
            userid = None
        else:
            userid = userid
        result = j.apps.system.usermanager.extensions.usermanager.usercreate(name=name, passwd=passwd, groups=groups, emails=emails, userid=userid)
        return result

    def userexists(self, name, **args):
        """
        param:name name
        result bool

        """
        return self.modelUser.exists("%s_%s"%(j.application.whoAmI.gid,name))

    def whoami(self, **kwargs):
        """
        result current user
        """
        ctx = kwargs["ctx"]
        return str(ctx.env['beaker.session']["user"])


    def userregister(self, name, passwd, emails, reference, remarks, config, **args):
        """
        param:name name of user
        param:passwd chosen passwd (will be stored hashed in DB)
        param:emails comma separated list of email addresses
        param:reference reference as used in other application using this API (optional)
        param:remarks free to be used field by client
        param:config free to be used field to store config information e.g. in json or xml format
        result bool

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method userregister")
