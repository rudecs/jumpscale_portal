import json

def generate_tags(line):
    tags = []
    state = 0
    for w in line.split(' '):
        if state == 0:
            obj = {}
        if w in ['AND', 'OR']:
            state = 1
            obj['conditions'] = w
        else:
            state = 0
            ss = w.split('=')
            obj['key'] = ss[0]
            obj['value'] = ss[1]
            tags.append(obj)
    return tags

def generate_groupby(line):
    tags = line.split(' ')
    groupby = []
    for tag in tags:
        obj = {'params':[tag],'type':'tag'}
        groupby.append(obj)
    groupby.append({'params':['$interval'],'type':'time'})
    return groupby


def main(j, args, params, tags, tasklet):
    page = args.page
    graphdata = args.cmdstr.format(**args.doc.appliedparams)
    scl = j.clients.osis.getNamespace('system')

    checksum = j.tools.hash.md5_string(graphdata)
    graphdata = j.core.hrd.get(content=graphdata)

    targets = graphdata.getDictFromPrefix('target')
    cfg = {'stack': False, 'fill': '1', 'percentage': False, "y_format": 'short', 'checksum': checksum}
    cfg.update(graphdata.getDictFromPrefix('cfg'))
    if 'dashboardtitle' not in cfg:
        cfg['dashboardtitle'] = checksum

    datasource = cfg.get('datasource')
    if datasource is None:
        # get location specific influxdb
        gid = int(args.doc.appliedparams.get('gid', '-1'))
        if gid != -1:
            grid = scl.grid.get(gid)
            datasource = 'controller_{}'.format(grid.name)
        else:
            datasource = 'influxdb_main'

    cfg['datasource'] = datasource

    targetsstr = ''
    grafanatargets = []

    for target in targets.values():
        target['value'] = target.get('value', 'value')
        targetvalue = {
                        "fields": [
                            {
                                "func": target['function'],
                                "name": target['value']
                            }
                        ],
                        "measurement": target['series'],
                        "alias": target['alias'],
                        "interval": target['interval'],
                      }

        if 'query' in target:
            targetvalue['query'] = target['query']

        if 'condition' in target:
            targetvalue['tags'] = generate_tags(target['condition'])

        if 'groupby' in target:
            targetvalue['groupByTags'] = target['groupby'].split(' ')
            targetvalue['groupBy'] = generate_groupby(target['groupby'])

        grafanatargets.append(targetvalue)
    cfg['target'] = targetsstr.strip(',')

    dashboard = {
      "id": None,
      "title": cfg['dashboardtitle'],
      "tags": [],
      "style": "dark",
      "timezone": "browser",
      "editable": False,
      "hideControls": True,
      "sharedCrosshair": False,
      "rows": [
        {
          "height": "250px",
          "panels": [
            {
              "title": cfg['title'],
              "error": False,
              "span": 12,
              "editable": False,
              "type": "graph",
              "id": 1,
              "datasource": cfg['datasource'],
              "renderer": "flot",
              "x-axis": True,
              "y-axis": True,
              "y_formats": [
                cfg['y_format'],
                cfg['y_format']
              ],
              "grid": {
                "leftLogBase": 1,
                "leftMax": None,
                "rightMax": None,
                "leftMin": None,
                "rightMin": None,
                "rightLogBase": 1,
                "threshold1": None,
                "threshold2": None,
                "threshold1Color": "rgba(216, 200, 27, 0.27)",
                "threshold2Color": "rgba(234, 112, 112, 0.22)"
              },
              "lines": True,
              "fill": 1,
              "linewidth": 2,
              "points": False,
              "pointradius": 5,
              "bars": False,
              "stack": cfg['stack'],
              "percentage": cfg['percentage'],
              "legend": {
                "show": True,
                "values": False,
                "min": False,
                "max": False,
                "current": False,
                "total": False,
                "avg": False
              },
              "NonePointMode": "connected",
              "steppedLine": False,
              "tooltip": {
                "value_type": "cumulative",
                "shared": True
              },
              "timeFrom": None,
              "timeShift": None,
              "targets": grafanatargets,
              }
           ],
          "title": cfg['title'],
          "collapse": False,
          "editable": False
        }
      ],
      "nav": [
        {
          "type": "timepicker",
          "collapse": False,
          "notice": False,
          "enable": True,
          "status": "Stable",
          "time_options": [
            "5m",
            "15m",
            "1h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d"
          ],
          "refresh_intervals": [
            "5s",
            "10s",
            "30s",
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d"
          ],
          "now": True
        }
      ],
      "time": {
        "from": "now-6h",
        "to": "now"
      },
      "templating": {
        "list": []
      },
      "annotations": {
        "list": []
      },
      "schemaVersion": 6,
      "version": 0,
      "links": []
    }

    grafclient = j.clients.grafana.getByInstance('main')
    result = grafclient.updateDashboard(dashboard)
    cfg['slug'] = result['slug']
    page.addHTML("""
        <iframe width="%(width)s" height="%(height)s" src="/grafana/dashboard-solo/db/%(slug)s?panelId=1&fullscreen&theme=light" frameborder="0"></iframe>""" % cfg)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
