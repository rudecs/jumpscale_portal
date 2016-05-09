from JumpScale import j
import time

class system_health(j.code.classGetBase()):

    """
    Alerts handler
    
    """

    def __init__(self):
        self.scl = j.clients.osis.getNamespace('system', j.core.portal.active.osis)
        self.acl = j.clients.agentcontroller.get()


    def run(self, nid=None, **kwargs):
        if nid:
            nid = int(nid)
            j.core.grid.healthchecker.runAllOnNode(nid, False)
        else:
            j.core.grid.healthchecker.runOnAllNodes(False)
        return "Scheduled healthcheck"

    def getDetailedStatus(self, nid, **kwargs):
        """
        get detailed status for a node
        param:nid id of node
        result json
        """
        now = time.time()
        nidint = int(nid)

        results = j.core.grid.healthchecker.fetchMonitoringOnNode(nidint)
        _, oldestdate = j.core.grid.healthchecker.getErrorsAndCheckTime(results)
        out = {}
        res = {'lastchecked': oldestdate, 'categories': out}

        noderesults = results.get(nidint, dict())
        for category, data in sorted(noderesults.items()):
            row = []
            categorystatus = "OK"
            skipcount = 0
            for dataitem in data:
                if isinstance(dataitem, dict):
                    status = dataitem.get('state')
                    if status == 'SKIPPED':
                        skipcount += 1
                    if categorystatus != 'ERROR' and status not in ['OK', 'SKIPPED']:
                        categorystatus = status
                    lastchecked = dataitem.get('lastchecked', '')
                    if lastchecked:
                        lastchecked = '%s ago' % j.base.time.getSecondsInHR(now - lastchecked)
                    interval = dataitem.get('interval')
                    if interval:
                        interval = j.base.time.getSecondsInHR(interval)
                    else:
                        interval = ''

                    message = dataitem.get('message', '')
                    row.append({'msg': message, 'last': lastchecked, 'interval': interval, 'status': status})
                else:
                    row.append(dataitem)
            if skipcount == len(data):
                categorystatus = 'SKIPPED'

            out[category] = {'status': categorystatus, 'data': row}
        return res

    def getOverallStatus(self, **kwargs):
        """
        get the status of the system
        result json
        """
        return {'state': j.core.grid.healthchecker.fetchState()}

    def getStatusSummary(self, **kwargs):
        """
        get the status summary for the nodes
        result json
        """
        rows = {}
        data = j.core.grid.healthchecker.fetchMonitoringOnAllNodes()
        errors, oldestdate = j.core.grid.healthchecker.getErrorsAndCheckTime(data)
        if len(data) > 0:
            for nid, checks in data.items():
                level = 0
                if nid in errors:
                    level = -1
                    categories = errors.get(nid, [])
                    runningstring = 'DEGRADED'
                else:
                    level = 0
                    categories = None
                    runningstring = 'RUNNING'
                status = checks.get('JSAgent', [{'state': 'UNKOWN'}])[0]
                if status and status['state'] != 'OK':
                    level = -2
                    runningstring = 'HALTED'
                gid = j.core.grid.healthchecker.getGID(nid)
                name = j.core.grid.healthchecker.getName(nid)
                row = {'level': level, 'gid': gid, 'nid': nid, 'status': runningstring, 'name': name}
                if categories:
                    row['categories'] = categories
                rows['%s_%s'%(gid, nid)] = row

        return rows