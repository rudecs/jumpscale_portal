import time
import os
import subprocess
from JumpScale import j
import JumpScale.portal

import sys

if __name__ == '__main__':
     
    if 'PORTAL_MAIN' in os.environ:
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
