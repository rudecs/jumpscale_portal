from JumpScale import j

def cb():
    from .Docgenerator import DocgeneratorFactory
    return DocgeneratorFactory()

j.base.loader.makeAvailable(j, 'tools')
j.tools._register('docgenerator', cb)
