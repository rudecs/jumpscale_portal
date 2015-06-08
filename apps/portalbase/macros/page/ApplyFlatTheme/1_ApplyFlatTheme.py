
def main(j, args, params, tags, tasklet):

    page = args.page
    params.extend(args)
    page.addHTMLHeader('''<link rel="shortcut icon" type="image/png" href="/system/.files/img/favicon.png">''')
    page.addCSS('/jslib/bootstrap/css/bootstrap-3-3-1.min.css')
    page.addCSS('/jslib/flatui/css/flat-ui.css')
    page.addCSS('/jslib/new-ui/new-ui.css')
    page.addCSS('/jslib/new-ui/oocss.css')

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
        
        $('link[href="/jslib/old/bootstrap/css/bootstrap.css"]').remove();
        $('link[href="/jslib/old/bootstrap/css/bootstrap-responsive.css"]').remove();
        $('link[href="/jslib/old/breadcrumbs/breadcrumbs.css"]').remove();
        $('link[href="/jslib/swagger/css/reset.css"]').remove();

        
        $('.nav-collapse.collapse').removeClass('nav-collapse').addClass('navbar-collapse');
        $('.btn.btn-navbar').replaceWith('<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".nav-collapse" aria-expanded="false">' +
            '<span class="sr-only">Toggle navigation</span>' +
            '<span class="icon-bar"></span>' +
            '<span class="icon-bar"></span>' +
            '<span class="icon-bar"></span>' +
          '</button>'
        );
        $('.brand').removeClass('brand').addClass('navbar-brand');
        $('.navbar-inner').addClass('navbar-form');
        $('.search-query').addClass('form-control');
        $('.newBreadcrumbArrow').removeClass('newBreadcrumbArrow separator').addClass('fui-arrow-right');

        $('.span1').removeClass('span1').addClass('col-md-1');
        $('.span2').removeClass('span2').addClass('col-md-2');
        $('.span3').removeClass('span3').addClass('col-md-3');
        $('.span4').removeClass('span4').addClass('col-md-4');
        $('.span5').removeClass('span5').addClass('col-md-5');
        $('.span6').removeClass('span6').addClass('col-md-6');
        $('.span7').removeClass('span7').addClass('col-md-7');
        $('.span8').removeClass('span8').addClass('col-md-8');
        $('.span9').removeClass('span9').addClass('col-md-9');
        $('.span10').removeClass('span10').addClass('col-md-10');
        $('.span11').removeClass('spa11').addClass('col-md-11');
        $('.span12').removeClass('span12').addClass('col-md-12');
    });
     ''')
    
    page.addCSS('/system/.files/css/flatTheme.css')

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
