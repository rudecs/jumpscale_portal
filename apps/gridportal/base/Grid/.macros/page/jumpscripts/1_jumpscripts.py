def main(j, args, params, tags, tasklet):
    page = args.page

    filters = dict()
    tagsmap = {
        'jsname': 'name',
        'jsorganization': 'organization',
    }

    fieldids = ['id', 'jsname', 'jsorganization', 'category', 'descr']
    for tag, val in args.tags.tags.iteritems():
        key = tagsmap.get(tag, tag)
        if tag in fieldids:
            val = args.getTag(tag)
            filters[key] = val
        else:
            val = args.getTag(tag)
            filters["tags"] = {"$regex": ("%s|(?=.*%s:%s)" % (filters["tags"]['$regex'], key, val))} if "tags" in filters else {"$regex": "(?=.*%s:%s)" % (key, val)}

    for k in filters.keys():
        if filters[k] is None:
            del filters[k]

    modifier = j.html.getPageModifierGridDataTables(page)

    def makeID(row, field):
        _id = row[field]
        link = "[%s|/grid/jumpscript?id=%s]" % (_id, _id)
        return link

    fields = [
        {'name': 'ID',
         'id': 'id',
         'value': makeID},
        {'name': 'Name',
         'id': 'name',
         'value': 'name'},
        {'name': 'Organization',
         'id': 'organization',
         'value': 'organization'},
        {'name': 'Category',
         'id': 'category',
         'value': 'category'},
        {'name': 'Description',
         'id': 'descr',
         'value': 'descr'},
    ]

    tableid = modifier.addTableFromModel('system', 'jumpscript', fields, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
