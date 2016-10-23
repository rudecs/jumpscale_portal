from JumpScale import j

class system_usermanager(j.code.classGetBase()):
    """
    get a user
    """
    def __init__(self):
        pass
        
        self._te={}
        self.actorname="usermanager"
        self.appname="system"
        #system_usermanager_osis.__init__(self)


    def authenticate(self, name, secret, **kwargs):
        """
        authenticate and return False if not successfull
        otherwise return secret for api
        param:name name
        param:secret md5 or passwd
        result str
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method authenticate")

    def create(self, username, password, groups, emails, domain, provider, **kwargs):
        """
        create a user
        param:username name of user
        param:password password optional when provider is set
        param:groups list of groups this user belongs to
        param:emails list of email addresses
        param:domain domain of user
        param:provider provider for this user
        result str,
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method create")

    def createGroup(self, name, domain, description, **kwargs):
        """
        create a group
        param:name name of group
        param:domain domain of group
        param:description description of group
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method createGroup")

    def delete(self, username, **kwargs):
        """
        Delete a user
        param:username name of the user
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method delete")

    def deleteGroup(self, id, **kwargs):
        """
        delete a group
        param:id id/name of group
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method deleteGroup")

    def editGroup(self, name, domain, description, users, **kwargs):
        """
        edit a group
        param:name name of group
        param:domain domain of group
        param:description description of group
        param:users list or comma seperate string of users
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method editGroup")

    def editUser(self, username, groups, password, emails, domain, **kwargs):
        """
        set Groups for a user
        param:username name of user
        param:groups list of groups this user belongs to
        param:password password for user
        param:emails list of email addresses
        param:domain Domain of user
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method editUser")

    def userexists(self, name, **kwargs):
        """
        param:name name
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method userexists")

    def userget(self, name, **kwargs):
        """
        param:name name of user
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method userget")

    def usergroupsget(self, user, **kwargs):
        """
        return list of groups in which user is member of
        param:user name of user
        result list(str)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method usergroupsget")

    def whoami(self, **kwargs):
        """
        return username
        result str
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method whoami")
