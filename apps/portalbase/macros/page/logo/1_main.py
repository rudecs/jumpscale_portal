
def main(j, args, params, tags, tasklet):

    page = args.page
    page.addBootstrap()    
    
    image = j.apps.system.logo.get()
    if image:
        page.logo = "data:image/jpeg;base64, {}".format(image)
    else:
        page.logo = args.cmdstr

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
