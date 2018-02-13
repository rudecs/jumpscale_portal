from JumpScale import j
from JumpScale.portal.portal.auth import auth
import base64

class system_logo(j.code.classGetBase()):

    def __init__(self):

        self.actorname = "logo"
        self.appname = "system"
        self.osiscl = j.core.portal.active.osis
        self.modelBlob = j.clients.osis.getCategory(self.osiscl, 'system', 'blob')

    def get(self, **kwargs):
        """
        get the logo
        param:name name of user
        """
        image = self.modelBlob.get('logo')
        return image


    @auth(['admin'])
    def set(self, image, **kwargs):
        img = image[image.keys()[0]]
        self.modelBlob.set(base64.b64encode(img.read()), 'logo')
        returncontent = "<script>window.location.replace(document.referrer);</script>"
        return returncontent

    @auth(['admin'])
    def delete(self, **kwargs):
        self.modelBlob.delete("logo")
        returncontent = "<script>window.location.replace(document.referrer);</script>"
        return returncontent
