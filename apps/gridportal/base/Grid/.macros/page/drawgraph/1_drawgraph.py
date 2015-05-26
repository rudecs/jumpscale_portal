def main(j, args, params, tags, tasklet):
    page = args.page
    graphdata = args.cmdstr.format(**args.doc.appliedparams)
    graphdata = j.core.hrd.get(content=graphdata)

    targets = graphdata.getDictFromPrefix('target')
    cfg = {'stack': 'false', 'fill': '1', 'percentage': 'false', "y_format": 'short'}
    cfg.update(graphdata.getDictFromPrefix('cfg'))

    targetsstr = ''

    for target in targets.values():
        target['value'] = target.get('value', 'value')
        targetsstr += """
                        {
                            "target": "randomWalk('random walk')",
                            "function":"%(function)s",
                            "column": "%(value)s",
                            "series": "%(series)s",
                            "query": "",
                            "alias": "%(alias)s",
                            "interval": "%(interval)s"
                        },""" % target
    cfg['target'] = targetsstr.strip(',')

    configuration = """
 {
    "title": "Grafana",
    "tags": [],
    "style": "light",
    "timezone": "browser",
    "editable": false,
    "rows": [
        {
            "title": "%(title)s",
            "height": "250px",
            "editable": false,
            "collapse": false,
            "collapsable": true,
            "panels": [
                {
                    "editable": false,
                    "type": "graph",
                    "x-axis": true,
                    "y-axis": true,
                    "scale": 1,
                    "y_formats": [
                        "%(y_format)s",
                        "short"
                    ],
                    "grid": {
                        "max": null,
                        "min": null,
                        "leftMax": null,
                        "rightMax": null,
                        "leftMin": null,
                        "rightMin": null,
                        "threshold1": null,
                        "threshold2": null,
                        "threshold1Color": "rgba(216,200,27,0.27)",
                        "threshold2Color": "rgba(234,112,112,0.22)"
                    },
                    "resolution": 100,
                    "lines": true,
                    "fill": %(fill)s,
                    "linewidth": 2,
                    "points": false,
                    "pointradius": 5,
                    "bars": false,
                    "stack": %(stack)s,
                    "spyable": true,
                    "options": false,
                    "legend": {
                        "show": true,
                        "values": false,
                        "min": false,
                        "max": false,
                        "current": false,
                        "total": false,
                        "avg": false
                    },
                    "interactive": true,
                    "legend_counts": true,
                    "timezone": "browser",
                    "percentage": %(percentage)s,
                    "zerofill": true,
                    "nullPointMode": "connected",
                    "steppedLine": false,
                    "tooltip": {
                        "value_type": "cumulative",
                        "query_as_alias": true
                    },
                    "targets": [
                        %(target)s
                    ],
                    "aliasColors": {},
                    "aliasYAxis": {},
                    "title": "%(title)s",
                    "datasource": null,
                    "renderer": "flot",
                    "annotate": {
                        "enable": false
                    }
                }
            ],
            "notice": false
        }
    ],
    "pulldowns": [
        {
            "type": "filtering",
            "collapse": false,
            "notice": false,
            "enable": false
        },
        {
            "type": "annotations",
            "enable": false
        }
    ],
    "nav": [
        {
            "type": "timepicker",
            "collapse": false,
            "notice": false,
            "enable": true,
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
            "now": true
        }
    ],
    "time": {
        "from": "now-1h",
        "to": "now"
    },
    "templating": {
        "list": []
    },
    "version": 2
}
""" % cfg

    checksum = j.tools.hash.md5_string(configuration)
    cfg['checksum'] = checksum
    path = j.system.fs.joinPaths(j.dirs.baseDir, 'apps', 'portals', 'jslib', 'grafana', 'app', 'dashboards', '%(checksum)s.json' % cfg)
    if not j.system.fs.exists(path):
        j.system.fs.writeFile(path, configuration)

    page.addHTML("""
        <iframe width="%(width)s" height="%(height)s" src="/jslib/grafana/iframe.html#/dashboard/file/%(checksum)s.json" frameborder="0"></iframe>""" % cfg)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
