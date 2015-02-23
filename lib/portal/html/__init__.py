from JumpScale import j

def cb():
    from .HtmlFactory import HtmlFactory
    return HtmlFactory()

j._register('html', cb)
