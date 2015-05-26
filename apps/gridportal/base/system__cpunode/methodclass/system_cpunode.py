from JumpScale import j
import os

class system_cpunode(j.code.classGetBase()):
    """
    API Actor api for managing cpu node creation and bootstraping
    """
    def __init__(self):
        self._te = {}
        self.actorname = "cpunode"
        self.appname = "system"
        #openvcloud_cpunode_osis.__init__(self)

    def init(self, **kwargs):
        """
        return the init script for creating a new node
        result str
        """
        _, portalAddrr = j.system.net.getDefaultIPConfig()
        script = """#!/bin/bash

PRIVPATH="$HOME/.ssh/id_dsa"
PUBPATH="$PRIVPATH.pub"
if [ ! -e "$PUBPATH" ]
then
    ssh-keygen -t dsa -f "$PRIVPATH" -P ''
fi
PUBKEY=`cat $PUBPATH`

curl -X POST -F "pubkey=$PUBKEY" -F "login=$USER" -F "hostname=$HOSTNAME" http://%s:82/restmachine/system/cpunode/create | bash"""
        ctx = kwargs["ctx"]
        headers = [('Content-Type', 'text/plain'), ]
        ctx.start_response("200", headers)
        return (script % portalAddrr).strip()

    def create(self, login, pubkey, hostname, **kwargs):
        """
        Create a new cpu node
        param:login login to connect to the node
        param:passwd password of the login given in argument
        param:pubkey public ssh key of the cpunode
        result str
        """
        sshkey = None
        loc = None
        ctx = kwargs["ctx"]
        headers = [('Content-Type', 'text/plain'), ]

        try:
            loc = j.atyourservice.get(name='location', instance='dev')
        except RuntimeError as e:
            if e.message.find('cannot find service') == -1:
                ctx.start_response("500", headers)
                return "echo %s" % e.message

        if loc is None:
            loc = j.atyourservice.new(name='location', instance='dev')
            loc.install()

        try:
            sshkey = j.atyourservice.get(name='sshkey', instance='dev', parent=loc)
        except RuntimeError as e:
            if e.message.find('cannot find service') == -1:
                ctx.start_response("500", headers)
                return "echo %s" % e.message

        if sshkey is None:
            data = {'instance.key.priv': ''}  # emtpy trigger autogeneration
            sshkey = j.atyourservice.new(name='sshkey', instance='dev', args=data, parent=loc)
            sshkey.install(deps=True)

        # remove service if already exists
        nodes = j.atyourservice.findServices(name='node.ssh', instance=hostname, parent=loc)
        for n in nodes:
            j.system.fs.removeDirTree(n.path)

        try:
            masterPort = self._findFreePort()
        except RuntimeError as e:
            ctx.start_response("500", headers)
            return "echo %s" % e.message

        nodePort = 22
        masterLogin = os.environ['USER']
        _, masterAddr = j.system.net.getDefaultIPConfig()
        data = {
            "instance.ip": "127.0.0.1",  # localhost cause we reverse ssh tunnel
            "instance.ssh.port": masterPort,
            'instance.sshkey': sshkey.instance,
            'instance.login': login,
            'instance.password': ""
        }
        node = j.atyourservice.new(name='node.ssh', instance='cpu1', args=data, parent=loc)
        node.init()

        # todo handle exeption here
        # todo make sure the key is valid
        authorized_keys_path = j.system.fs.joinPaths(os.environ['HOME'], '.ssh/authorized_keys')
        j.system.fs.writeFile(authorized_keys_path, pubkey, append=True)

        # start jscript that will install the node
        self._scheduleInstall(node)

        script = """
#!/bin/bash
autossh -f -NR {masterPort}:localhost:{nodePort} {masterLogin}@{masterAddr}
"""
        ctx.start_response("201", headers)
        return script.format(
            masterPort=masterPort,
            nodePort=nodePort,
            masterLogin=masterLogin,
            masterAddr=masterAddr
        )

    def _findFreePort(self):
        port_range = [i for i in xrange(2000, 2500)]
        nodes = j.atyourservice.findServices(name='node.ssh')
        taken_port = [n.hrd.get('instance.ssh.port') for n in nodes]
        free_port = [p for p in port_range if p not in taken_port]
        for p in sorted(free_port):
            if not j.system.net.checkListenPort(p):
                return p
        raise RuntimeError('no available port to connect to')

    def _scheduleInstall(self, node):
        args = {
            'node': str(node),
            'parent': str(node.parent)
        }
        clients = j.atyourservice.findServices(name='agentcontroller_client')
        if len(clients) <= 0:
            raise RuntimeError('no agentcontroller client installed')
        cl = j.clients.agentcontroller.getByInstance(clients[0].instance)

        gid, nid, _ = j.application.whoAmI
        cl.executeJumpscript("jumpscale", "cpunode_install", nid=nid, args=args, all=False, timeout=300, wait=False, gid=gid, errorreport=True, transporttimeout=5)
