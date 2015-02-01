from JumpScale import j

from .PortalFactory import PortalFactory, PortalFactoryClient
j.base.loader.makeAvailable(j, 'core')
j.base.loader.makeAvailable(j, 'clients')
j.core.portal = PortalFactory()
j.clients.portal = PortalFactoryClient()
