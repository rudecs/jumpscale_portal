from JumpScale import j

def portalloader():
    from .PortalLoaderFactory import PortalLoaderFactory
    return PortalLoaderFactory()

j.base.loader.makeAvailable(j, 'core')
j.core._register('portalloader', portalloader)
