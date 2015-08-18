def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    out="{{datatables_use}}}}\n\n"

    out+="||Name||Description||Domain||Active||\n"
    users = j.core.portal.active.auth.listGroups()
    for user in users:
        out += "|[%(id)s|group?id=%(id)s]|%(description)s|%(domain)s|%(active)s|\n" % user

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
