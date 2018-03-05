# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey
monkey.patch_all()
monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_thread()
monkey.patch_time()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time

import os
import subprocess
from JumpScale import j
import JumpScale.portal

if __name__ == '__main__':
    if 'PORTAL_MAIN' in os.environ:
        while not j.clients.redis.isRunning('system'):
            time.sleep(1)
            print "cannot connect to redis system, will keep on trying forever, please start redis system"
        args=sys.argv
        instance=args[1]

        j.application.instanceconfig = j.application.getAppInstanceHRD(name="portal",instance=instance)

        j.application.start("portal")

        server=j.core.portal.getServer()
        server.start()

        j.application.stop()
    else:
        while True:
            env = os.environ.copy()
            env['PORTAL_MAIN'] = 'true'
            print('Loading portal')
            try:
                exitcode = subprocess.call([sys.executable] + sys.argv, env=env)
                if exitcode != 3:
                    j.application.stop(exitcode)
            except KeyboardInterrupt:
                j.application.stop(0)
