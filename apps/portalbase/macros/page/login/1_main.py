def main(j, args, params, tags, tasklet):
    page = args.page
    page.addCSS("/jslib/bootstrap/css/bootstrap-3-3-1.min.css")
    page.addCSS("/jslib/old/bootstrap/css/bootstrap-responsive.css")
    page.addCSS("/jslib/flatui/css/flat-ui.css")
    page.addCSS("/jslib/font-awesome/css/font-awesome.min.css")
    page.addCSS("/jslib/bootstrap/css/bootstrap-social.css")
    page.addHTMLHeader('''<link rel="shortcut icon" type="image/png" href="/system/.files/img/favicon.png">''')
    
    page.addCSS(cssContent='''
      body{
        background-color: #34495e !important;
      }
      .login-form:before{
        border-width: 0;
      }
      .login-screen{
        padding: 0;
      }
      h4{
        color: #fff;
        text-align: center;
      }
      .span12, .form-signin{
        margin-top: 10%;
      }
      .login-field{
        height: 40px !important;
      }
      .fixFirefoxSizing{
        transform: scale(0.8, 0.8);
        transform-origin: 45% 0px 0px;
      }
      .btn-social{
        text-shadow: 0 0 0 rgba(255, 255, 255, 0.75) !important;
        margin-bottom: 10px;
        text-align: center;
      }
      .btn-social span{
        margin-left: -20px;
      }
      .login-screen{
        background-color: #34495e;
      }
      .login-form .login-field:focus{
        border-color: #5D88B3;
      }
      .login-form .login-field:focus + .login-field-icon{
        color: #5D88B3;
      }
      .btn-primary{
        background-color: #5D88B3;
      }
      .btn-primary:hover{
        background-color: #4A7198;
      }
    ''')
    page.addJS(jsContent='''
      $( function () {
        $('body').addClass('flatTheme');
        // fix firefox elements size on windows
        var operatingSystem = navigator.platform;
        if(operatingSystem.indexOf('Win') >= 0 && $.browser.mozilla == true){
            $('body').addClass('fixFirefoxSizing');
        }else{
            $('body').addClass('removeTransform');
        }
      });
    ''')
    head = """
<title>Login</title>
	"""

    body = """
    <form id="loginform" class="form-signin container" method="post" action="/system/login">
       <h4>Access Denied Please Login</h4>
       <div class="col-sm-offset-3 col-md-6 login-screen">
        <div class="login-form">
          <div class="form-group">
            <input type="text" class="form-control login-field" value="" name="user_login_" placeholder="Enter your username" id="login-name">
            <label class="login-field-icon fui-user" for="login-name"></label>
          </div>

          <div class="form-group">
            <input type="password" class="form-control login-field" value="" name="passwd" placeholder="Password" id="login-pass">
            <label class="login-field-icon fui-lock" for="login-pass"></label>
          </div>

          <button class="btn btn-primary btn-lg btn-block mbm" type="submit">Sign in</button>"""
    
    oauth_instances = j.core.config.list('oauth_client')
    for instance in oauth_instances:
        name = instance
        body += '''
        <a class="btn btn-block btn-social btn-%s" href=/restmachine/system/oauth/authenticate?type=%s>
          <i class="fa fa-%s"></i> <span>Login with %s</span>
        </a>''' % (name, name, name, name.capitalize())
    
    body += """
        </div>
      </div>
    </form>
	"""
    if args.tags.tagExists("jumptopath"):
        jumpto = args.tags.tagGet("jumptopath")
    else:
        jumpto = args.requestContext.path
        if jumpto.find("wiki") == 0:
            jumpto = jumpto[5:].strip("/")

    querystr = args.requestContext.env['QUERY_STRING']

    session = args.requestContext.env['beaker.session']
    session["querystr"] = querystr
    session.save()

    # if jumpto=="$$path":
        # path unknown
        # jumpto=""

    page.addBootstrap()
    page.addHTMLHeader(head)
    page.body += body
    page.body = page.body.replace("$$path", jumpto)
    if querystr:
        querystr = "?%s" % querystr
    page.body = page.body.replace("$$querystr", querystr)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
