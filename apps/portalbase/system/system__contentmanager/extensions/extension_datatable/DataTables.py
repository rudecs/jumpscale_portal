from JumpScale import j
from JumpScale.portal.portal import exceptions
from JumpScale.portal.docgenerator.Confluence2HTML import Confluence2HTML
import copy
import cgi
import json

class DataTables():

    def __init__(self):
        self.inited = False
        self.cache = j.db.keyvaluestore.getMemoryStore('datatables')
        self._osiscl =j.core.portal.active.osis
        self._catclient = dict()

    def getClient(self, namespace, category):
        key = '%s_%s' % (namespace, category)
        if key in self._catclient:
            return self._catclient[key]
        client = j.clients.osis.getCategory(self._osiscl, namespace, category)
        self._catclient[key] = client
        return client

    def getTableDefFromActorModel(self, appname, actorname, modelname, excludes=[]):
        """
        @return fields : array where int of each col shows position in the listProps e.g. [3,4]
              means only col 3 & 4 from listprops are levant, you can also use it to define the order
              there can be special columns added which are wiki templates to form e.g. an url or call a macro, formatted as a string
              e.g. [3,4,"{{amacro: name:$3 descr:$4}}","[$1|$3]"]
        @return fieldids: ids to be used for the fields ["name","descr","remarks","link"]
        @return fieldnames: names to be used for the fields ["Name","Description","Remarks","Link"], can be manipulated for e.g. translation
        """
        actor, model = self.getActorModel(appname, actorname, modelname)
        excludes = [item.lower() for item in excludes]
        fields = []
        fieldids = []
        fieldnames = []
        counter = 0
        iddone = False

        def getGuidPos():
            if "guid" in model.listProps:
                pos = model.listProps.index("guid")
                return pos
            raise RuntimeError("Could not find position of guid in %s %s %s" % (appname, actorname, modelname))
        for prop in model.listProps:
            fprop = counter
            lprop = prop.lower().strip().replace(" ", "")
            if lprop not in excludes:
                # if lprop.find("id")==0 and iddone==False:
                #     fprop="[$%s|%s]"%(counter,"/%s/%s/view_%s?guid=$%s"%(appname,actorname,modelname,getGuidPos()))
                #     iddone=True
                # if lprop.find("name") != -1 and iddone==False and guidpos != None:
                #     fprop="[$%s|%s]"%(counter,"/%s/%s/view_%s?guid=$%s"%(appname,actorname,modelname,getGuidPos()))
                #     iddone=True
                fprop = "[$%s|%s]" % (counter, "/space_%s__%s/form_%s?guid=$%s" % (appname, actorname, modelname, getGuidPos()))
                iddone = True
                fields.append(fprop)
                fieldids.append(lprop)
                fieldnames.append(prop)
            counter += 1

        return actor, model, fields, fieldids, fieldnames

    def storInCache(self, **kwargs):
        cacheinfo = kwargs.copy()
        key = j.base.idgenerator.generateGUID()
        self.cache.cacheSet(key, cacheinfo)
        return key

    def getFromCache(self, key):
        return self.cache.cacheGet(key)

    def executeMacro(self, row, field):

        try:
            for match in j.codetools.regex.getRegexMatches("\$\d*", field).matches:
                nr = int(match.founditem.replace("$", ""))
                field = field.replace(match.founditem, row[nr])
        except:
            raise RuntimeError("Cannot process macro string for row, row was %s, field was %s" % (row, field))

        field = field % row
        field = Confluence2HTML.findLinks(field)
        if field.find("{{") != -1:
            field = j.core.portal.active.macroexecutorPage.processMacrosInWikiContent(field)

        return field

    def getData(self, namespace, category, key, **kwargs):
        try:
            datainfo = self.getFromCache(key)
        except:
            raise exceptions.Gone('Table is not available anymore. Please refresh')
        fieldids = datainfo['fieldids']
        fieldvalues = datainfo['fieldvalues'] or fieldids
        filters = datainfo["filters"] or dict()
        nativequery = datainfo.get('nativequery') or dict()
        nativequery = copy.deepcopy(nativequery)
        filters = filters.copy()
        nativequery.update(filters)
        fullquery = {'$query': nativequery}

        client = self.getClient(namespace, category)

        #pagin
        start = kwargs['iDisplayStart']
        size = kwargs['iDisplayLength']


        #sort
        sort = []
        if kwargs['iSortCol_0']:
            for i in range(int(kwargs['iSortingCols'])):
                colidx = kwargs['iSortCol_%s' % i]
                key = 'bSortable_%s' % colidx
                if kwargs[key] == 'true':
                    colname = fieldids[int(colidx)-1]
                    sort.append((colname,  1 if kwargs['sSortDir_%s' % i] == 'asc' else -1))
        if sort:
            fullquery['$orderby'] = sort

        def getRegexQuery(value):
            regextmpl = '%s'
            if value.startswith('!'):
                value = value[1:]
                if value:
                    regextmpl = '^(?!.*%s).*$'
            query = {'$regex': regextmpl % value, '$options': 'i'}
            return query

        #filters
        partials = dict()
        for x in range(len(fieldids)):
            svalue = kwargs.get('sSearch_%s' % x)
            if kwargs.get('bSearchable_%s' % x) == 'true' and svalue:
                fieldname = fieldids[x]
                if svalue.isdigit():
                    if fieldname not in filters:
                        nativequery[fieldname] = int(svalue)
                else:
                    try:
                        q = json.loads(svalue)
                        if isinstance(q, dict):
                            nativequery[fieldname] = q
                        else:
                            nativequery[fieldname] = getRegexQuery(svalue)
                    except:
                        nativequery[fieldname] = getRegexQuery(svalue)


        #top search field
        if 'sSearch' in kwargs and kwargs['sSearch']:
            orquery = []
            nativequery['$or'] = orquery
            for idname in fieldids:
                orquery.append({idname: getRegexQuery(kwargs['sSearch'])})

        queryresult = client.search(fullquery, size=size, start=start)
        total = queryresult[0]
        inn = queryresult[1:]
        result = {}
        result["sEcho"] = int(kwargs.get('sEcho', 1))
        result["iTotalRecords"] = total
        result["iTotalDisplayRecords"] = total
        result["data"] = []
        for row in inn:
            r = [row.get('id', 'NA')]
            for field, fieldid in zip(fieldvalues, fieldids):
                if field in row or j.basetype.integer.check(field):
                    value = row[field]
                    if isinstance(value, basestring):
                        value = cgi.escape(value)
                    r.append(value)
                elif j.basetype.string.check(field):
                    r.append(self.executeMacro(row, field))
                else:
                    # is function
                    field = field(row, fieldid)
                    field = field or ' '
                    field = Confluence2HTML.findLinks(field)
                    r.append(field)

            result["data"].append(r)

        return result
