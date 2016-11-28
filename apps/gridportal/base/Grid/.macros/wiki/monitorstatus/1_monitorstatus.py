
def main(j, args, params, tags, tasklet):
    doc = args.doc
    import time
    now = time.time()
    nid = args.getTag('nid')
    nidint = int(nid)

    out = list()
    classmap = {'OK': 'success',
                'WARNING': 'warning',
                'EXPIRED': 'warning',
                'UNKNOWN': 'default',
                'HALTED': 'danger',
                'ERROR': 'danger'}

    def makeStatusLabel(status, guid=None, direction='left'):
        html = '<span class="label label-%s pull-%s status-label">%s</span>' % (classmap.get(status, 'default'), direction, status)
        if guid:
            html = '<a href="/grid/job?id=%s">%s</a>' % (guid, html)
        return html

    def addAction(cmd):
        if not cmd:
            return ''
        action = "{{action id:action-RefreshHealth class:'glyphicon glyphicon-refresh pull-right' data-cmd:'%s' label:''}}" % cmd
        return action

    results = j.core.grid.healthchecker.fetchMonitoringOnNode(nidint)
    _, oldestdate = j.core.grid.healthchecker.getErrorsAndCheckTime(results)

    out.append('Node was last checked at: {{ts:%s}}' % oldestdate)
    out.append('''
{{jscript:
$(function () {
    $('#accordion td:first-child').each(function() {
        var $this = $(this);
        $this.attr('title', $this.text());
    });
});
}}
''')

    out.append('{{html: <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">}}')
    noderesults = results.get(nidint, dict())
    for category, data in sorted(noderesults.items()):
        sectionid = 'collapse_%s' % category.replace(' ', '_')
        headingid = 'heading_%s' % category
        table = "||Message||Error Start||Last Executed||Interval||Status||\n"
        categorystatus = "OK"
        skipcount = 0
        for dataitem in data:
            if isinstance(dataitem, dict):
                status = dataitem.get('state')
                if status == 'SKIPPED':
                    skipcount += 1
                if categorystatus != 'ERROR' and status not in ['OK', 'SKIPPED']:
                    categorystatus = status
                lasterror = dataitem.get('lasterror', '') or ''
                if lasterror:
                    lasterror = '%s ago' % j.base.time.getSecondsInHR(now - lasterror)
                lastchecked = dataitem.get('lastchecked', '')
                status = makeStatusLabel(status, dataitem.get('guid'))
                if lastchecked:
                    lastchecked = '%s ago' % j.base.time.getSecondsInHR(now - lastchecked)
                interval = dataitem.get('interval')
                if interval:
                    interval = j.base.time.getSecondsInHR(interval)
                else:
                    interval = ''

                message = dataitem.get('message', '')
                cmd = dataitem.get('cmd')
                if cmd:
                    jobcategory, jobcmd = cmd.split('_', 1)
                    message = '[%(msg)s|/grid/jobs?nid=%(nid)s&cmd=%(jobcmd)s&category=%(category)s]' % {
                        'jobcmd': jobcmd,
                        'nid': nid,
                        'msg': message,
                        'category': jobcategory, }
                row = '|%(msg)s |%(lasterror)s |%(last)s |  %(interval)s| {{html: %(status)s}} %(refresh)s  |\n'
                table += row % {'msg': message,
                                'lasterror': lasterror,
                                'last': lastchecked,
                                'interval': interval,
                                'status': status,
                                'refresh': addAction(cmd)}
            else:
                table += dataitem
        if skipcount == len(data):
            categorystatus = 'SKIPPED'
        html = '''{{html:
<div class="panel panel-default">
    <div class="panel-heading" role="tab" id="%(headingid)s">
        <h4 class="panel-title">
            <a data-toggle="collapse" data-parent="#accordion" href="#%(sectionid)s" aria-expanded="false" aria-controls="%(sectionid)s">
                %(category)s
            </a>
            %(status)s
        </h4>
    </div>
    <div id="%(sectionid)s" class="panel-collapse collapse" role="tabpanel" aria-labelledby="%(headingid)s">
        <div class="panel-body">
}}
%(table)s
{{html:
        </div>
    </div>
</div>
}}
''' % {'headingid': headingid, 'sectionid': sectionid, 'table': table,
         'category': category, 'status': makeStatusLabel(categorystatus, direction='right')}

        out.append(html)

    out.append('{{html: </div>}}')

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
