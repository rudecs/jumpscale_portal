def main(j, args, params, tags, tasklet):
    page = args.page

    searchbox = """
        <form id=searchbox class=searchbox action="/cbgrid/search/" style='float: left; padding: 0px; margin: 0px 0; box-sizing: border-box;'>
            <input name="q" type="text" placeholder="Search.." id="q", autofocus>
        </form>
    """
    page.body = page.body.replace("$$$searchbox", searchbox)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True

