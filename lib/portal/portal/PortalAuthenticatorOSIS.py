from JumpScale import j
from JumpScale.portal.portal import exceptions
import time
import re
import random

class PortalAuthenticatorOSIS(object):

    def __init__(self, osis):
        self.osisuser = j.clients.osis.getCategory(osis, "system", "user")
        self.osisgroup = j.clients.osis.getCategory(osis, "system", "group")
        self.key2user = {user['authkey']: user['id'] for user in self.osisuser.simpleSearch({}, nativequery={'authkey': {'$ne': ''}})}

    def getUserFromKey(self,key):
        if not key in self.key2user:
            return "guest"
        return self.key2user[key]

    def _getkey(self, username, osis):
        results = osis.simpleSearch({'id': username}, withguid=True)
        if results:
            return results[0]['guid']
        else:
            return None

    def getUserInfo(self, user):
        key = self._getkey(user, self.osisuser)
        if not key:
            return None
        return self.osisuser.get(key)

    def getGroupInfo(self, groupname):
        key = self._getkey(groupname, self.osisgroup)
        if not key:
            return None
        return self.osisgroup.get(key)

    def userExists(self, user):
        return self._getkey(user, self.osisuser) is not None

    def _isValidUserName(self, username):
        r = re.compile('^[a-z0-9]{1,20}$')
        return r.match(username) is not None

    def _isValidEmailAddress(self, emailaddress):
        r = re.compile('^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$')
        return r.match(emailaddress) is not None

    def _isValidPassword(self, password):
        if len(password) < 8 or len (password) > 80:
            return False
        return re.search(r"\s",password) is None

    def createUser(self, username, password, email, groups, domain):
        if not self._isValidUserName(username):
            raise exceptions.BadRequest('Username may not exceed 20 characters and may '
                                        'only contain a-z and 0-9')
        else:
            if self.osisuser.search({'id': username})[1:]:
                    raise exceptions.Conflict('Username %s is already exists' % username)

        if not email:
            raise exceptions.BadRequest('Email address cannot be empty.')
        else:
            for address in email:
                if not self._isValidEmailAddress(address):
                    raise exceptions.BadRequest('Email address %s is in an invalid format'
                                                % address)
                if self.osisuser.search({'emails': address})[1:]:
                    raise exceptions.Conflict('Email address %s is already registered in the '
                                              'system' % address)

        user = self.osisuser.new()
        user.id = username
        user.groups = groups
        user.emails = email
        user.domain = domain
        if not password:
            password = str(random.random())
        elif not self._isValidPassword(password):
            raise exceptions.BadRequest("Password should have at least 8 characters and not more "
                                        "than 60 characters.")

        user.passwd = j.tools.hash.md5_string(password)
        return self.osisuser.set(user)

    def updateUser(self, username, password, email, groups, domain):
        users = self.osisuser.search({'id': username})[1:]
        if not users:
            raise exceptions.NotFound('Email address cannot be empty.')
        else:
            user = self.osisuser.get(users[0]['guid'])

        if not email:
            raise exceptions.BadRequest('Email address cannot be empty.')
        else:
            for address in email:
                if not self._isValidEmailAddress(address):
                    raise exceptions.BadRequest('Email address %s is in an invalid format'
                                                % address)
                if address not in user.emails and self.osisuser.search({'emails': address})[1:]:
                    raise exceptions.Conflict('Email address %s is already registered in the '
                                              'system with a different username' % address)
            user.emails = email

        user.groups = groups

        if domain:
            user.domain = domain

        if password:
            user.passwd = j.tools.hash.md5_string(password)
        return self.osisuser.set(user)

    def listUsers(self):
        return self.osisuser.simpleSearch({})

    def listGroups(self):
        return self.osisgroup.simpleSearch({})

    def getGroups(self,user):
        try:
            userinfo = self.getUserInfo(user).__dict__
            return userinfo['groups'] + ["all"]
        except:
            return ["guest","guests"]

    def loadFromLocalConfig(self):
        #@tddo load from users.cfg & populate in osis
        #see jsuser for example
        pass

    def authenticate(self,login,passwd):
        """
        """
        login = login[0] if isinstance(login, list) else login
        passwd = passwd[0] if isinstance(passwd, list) else passwd
        result=self.osisuser.authenticate(name=login, passwd=passwd)
        return result['authenticated']

    def getUserSpaceRights(self, username, space, **kwargs):
        spaceobject = kwargs['spaceobject']
        groupsusers = set(self.getGroups(username))

        for groupuser in groupsusers:
            if groupuser in spaceobject.model.acl:
                right = spaceobject.model.acl[groupuser]
                if right == "*":
                    return username, "rwa"
                return username, right

        # No rights .. check guest
        rights = spaceobject.model.acl.get('guest', '')
        return username, rights

    def getUserSpaces(self, username, **kwargs):
        spaceloader = kwargs['spaceloader']
        return [ x.model.id.lower() for x in  spaceloader.spaces.values()]
