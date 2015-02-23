from JumpScale import j

def docpre():
    from .DocPreprocessorFactory import DocPreprocessorFactory
    return DocPreprocessorFactory()

def docparser():
    from .DocParser import DocParser
    return DocParser()

j.base.loader.makeAvailable(j, 'tools')
j.tools._register('docpreprocessor', docpre)
j.tools._register('docpreprocessorparser', docparser)
