def main(j, args, params, tags, tasklet):
    page = args.page
    html = """
    <form class="form-horizontal" enctype="multipart/form-data" method="post" action="/restmachine/system/logo/set">

<div class="form-group">

<label for="image" class="col-sm-2 control-label">Logo</label>

<div class="col-sm-8">

<input type="file" required="true" class="form-control" id="image" name="image" placeholder="Upload your logo here">
</div>

</div>

<div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-primary">upload</button>
    </div>
  </div>

</form>

    """
    page.addHTML(html)
    image = image = j.apps.system.logo.get()
    if image:
        img = '<div class="col-sm-offset-2 col-sm-8"> <img alt="logo" src="data:image/jpeg;base64, {}" width="90px" hight="38px"> </div>'.format(image)
        page.addHTML(img)
        html_delete = """
        <form class="form-horizontal" method="post" action="/restmachine/system/logo/delete">
<div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-default">Delete</button>
    </div>
  </div>
</form>
        """
        page.addHTML(html_delete)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
