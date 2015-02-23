from JumpScale import j

def portalfactory():
    from .PortalFactory import PortalFactory
    return PortalFactory()

def portalclientfactory():
    from .PortalFactory import PortalFactoryClient
    return PortalFactoryClient()

j.base.loader.makeAvailable(j, 'core')
j.base.loader.makeAvailable(j, 'clients')
j.core._register('portal', portalfactory)
j.clients._register('portal', portalclientfactory)
