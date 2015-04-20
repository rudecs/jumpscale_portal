from JumpScale import j

def cb():
    from .imagelib.ImageLib import ImageLib
    return ImageLib()

j.base.loader.makeAvailable(j, 'tools')
j.tools._register('imagelib', cb)