from JumpScale import j
import time
class PortalAuthenticatorOSIS():

    def __init__(self, osis):
        self.osis=j.clients.osis.getCategory(osis,"system","user")
        self.osisgroups=j.clients.osis.getCategory(osis,"system","group")
        self.key2user={user['authkey']:user['id'] for user in self.osis.simpleSearch({}, nativequery={'authkey':{'$ne': ''}})}
        
    def existsKey(self,key):
        return key in self.key2user
        
    def getUserFromKey(self,key):
        if not self.existsKey(key):
            return "guest"
        return self.key2user[key]

    def _getkey(self, username, osis):
        results = osis.simpleSearch({'id': username}, withguid=True)
        if results:
            return results[0]['guid']
        else:
            return "%s_%s" % (j.application.whoAmI.gid, username)

    def getUserInfo(self, user):
        return self.osis.get(self._getkey(user, self.osis))

    def getGroupInfo(self, groupname):
        return self.osisgroups.get(self._getkey(groupname, self.osisgroups))

    def userExists(self, user):
        return self.osis.exists(self._getkey(user, self.osis))

    def createUser(self, username, password, email, groups, domain):
        user = self.osis.new()
        user.id=username
        if isinstance(groups, str):
            groups = [groups]
        user.groups=groups
        user.emails=email
        user.domain=domain
        user.passwd=j.tools.hash.md5_string(password)
        self.osis.set(user)

    def listUsers(self):
        return self.osis.simpleSearch({})

    def listGroups(self):
        return self.osisgroups.simpleSearch({})

    def getGroups(self,user):
        try:
            userinfo = self.getUserInfo(user).__dict__
            return userinfo['groups']
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
        result=self.osis.authenticate(name=login,passwd=passwd)
        return result['authenticated']
