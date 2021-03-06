import os


def main(j, args, params, tags, tasklet):

    page = args.page
    params.result = page

    page.addJS("/jslib/old/bootstrap-image-gallery/js/load-image.min.js")
    page.addJS("/jslib/old/bootstrap-image-gallery/js/bootstrap-image-gallery.min.js")
    page.addCSS("/jslib/old/bootstrap-image-gallery/css/bootstrap-image-gallery.min.css")
    C = """<div class="container-fluid"> 
    <div id="gallery" data-toggle="modal-gallery" data-target="#modal-gallery">"""
    pars = args.expandParamsAsDict()

    """
    This is code for using buckets can be extented later.
    buckets = j.core.portal.active.bucketsloader.buckets
    if pars.has_key('picturebucket') and pars['picturebucket'] in buckets:
        bucket = buckets[pars['picturebucket']]
        files = j.system.fs.listFilesInDir(bucket.model.path)
    else:
        files = []
    """
    space = j.core.portal.active.spacesloader.spaces[args.doc.getSpaceName()]
    imagedir = j.system.fs.joinPaths(space.model.path, '.files', 'img')
    if 'title' not in pars:
        title = ""
    else:
        title = pars['title']
    if 'picturedir' in pars:
        baseurlpath = "$$space/.files/img/%s" % pars['picturedir']
        fullimagepath = j.system.fs.joinPaths(imagedir, pars['picturedir'])
    else:
        baseurlpath = "images/$$space"
        localpath = args.doc.path
        fullimagepath = j.system.fs.getDirName(localpath)

    allfiles = j.system.fs.listFilesInDir(fullimagepath, filter="*.jpg", case_sensitivity='insensitive')
    allfiles += (j.system.fs.listFilesInDir(fullimagepath, filter="*.png", case_sensitivity='insensitive'))
    allfiles += (j.system.fs.listFilesInDir(fullimagepath, filter="*.bmp", case_sensitivity='insensitive'))
    allfiles += (j.system.fs.listFilesInDir(fullimagepath, filter="*.jpeg", case_sensitivity='insensitive'))
    allfiles += (j.system.fs.listFilesInDir(fullimagepath, filter="*.gif", case_sensitivity='insensitive'))

    smallfiles = j.system.fs.listFilesInDir(fullimagepath, filter="s_*.*")
    bigfiles = [x for x in allfiles if x not in smallfiles]

    thumb_size = pars.get('thumb_size', args.doc.docparams.get('thumb_size', '150x100'))

    thumb_size = [int(x) for x in thumb_size.split('x')]

    for i in bigfiles:
        basefile = j.system.fs.getBaseName(i)
        bigpath = "/%s/%s" % (baseurlpath.strip('/'), basefile)

        smallpath = "/%s/s_%sx%s_%s" % (baseurlpath, thumb_size[0], thumb_size[1], basefile)

        #link = '<a data-gallery = "gallery" data-href=%s title=%s><img src=%s></a>' % (bigpath, title, smallpath)

        # Generate a thumbnail from the existing image
        thumbnail_path = os.path.join(fullimagepath, 's_{0}x{1}_{2}'.format(thumb_size[0], thumb_size[1], basefile))
        if not os.path.exists(os.path.dirname(thumbnail_path)):
            os.makedirs(os.path.dirname(thumbnail_path))
        if not j.system.fs.exists(thumbnail_path):
            j.tools.imagelib.resize(i, thumbnail_path, width=thumb_size[0], overwrite=False)
        link = '<a data-gallery = "gallery" data-href=%s title=%s><img src="%s" /></a>' % (bigpath, title, smallpath, )
        C += link

    C += '</div></div>'

    C += """
    <div id="modal-gallery" class="modal modal-gallery hide fade modal-loading modal-fullscreen" tabindex="-1"  aria-hidden="true">
    <div class="modal-header">
        <a class="close" data-dismiss="modal">&times;</a>
        <h3 class="modal-title"></h3>
    </div>
    <div class="modal-body"><div class="modal-image"></div></div>
    </div>
    """
    page.addMessage(C)
    return params


def match(j, args, params, tags, tasklet):
    return True
