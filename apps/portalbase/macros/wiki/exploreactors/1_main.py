import os


def main(j, args, params, tags, tasklet):
    params.merge(args)

    out = ""

    actors = j.core.portal.active.actorsloader.id2object

    for actorname in sorted(actors.keys()):
        model = actors[actorname].model  # @todo security breach
        path = os.path.abspath(model.path)
        if not j.system.fs.exists(path):
            j.system.fs.createDir(path)
        path = path.replace(":", "___")
        # out+="|[%s | /system/Explorer/?path=%s] |[reload | /system/reloadactor/?name=%s]|\n" % (model.id,path,model.id)
        out += "|%s|[Spec|/system/Explorer?ppath=%s]|[Actions|/system/Explorer?ppath=%s]|\n" % (actorname.capitalize(),
                                                               j.system.fs.joinPaths(path, 'specs'),
                                                               j.system.fs.joinPaths(path, 'methodclass'))

    params.result = out

    params.result = (params.result, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
