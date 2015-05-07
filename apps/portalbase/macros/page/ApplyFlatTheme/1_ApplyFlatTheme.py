
def main(j, args, params, tags, tasklet):

    page = args.page
    params.extend(args)

    page.addCSS('/jslib/bootstrap/css/bootstrap-3-3-1.min.css')
    page.addCSS('/jslib/flatui/css/flat-ui.css')
    page.addCSS('/jslib/new-ui/new-ui.css')

    page.addJS(jsContent='''
        $( function () {

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

    page.addCSS(cssContent=''' 
    /* General styling */
    body{
        font-size: 15px;
        padding-top: 80px !important;
        padding-bottom: 0 !important;
        margin-left: 0;
        margin-top: 0;
    }
    .fixFirefoxSizing{
        transform: scale(0.8, 0.8);
        transform-origin: 45% 0px 0px;
    }
    .removeTransform{
        transform: none;
        transform-origin: 0;
    }
    body input[type=text]{
        border: 2px solid #bdc3c7;
        color: #34495e;
        font-family: "Lato", Helvetica, Arial, sans-serif;
        font-size: 14px;
        line-height: 1.467;
        padding: 6px 10px;
        height: 35px;
        -webkit-appearance: none;
        border-radius: 6px;
        -webkit-box-shadow: none;
        box-shadow: none;
        -webkit-transition: border .25s linear, color .25s linear, background-color .25s linear;
        transition: border .25s linear, color .25s linear, background-color .25s linear;        
    }
    body input[type=text]:focus{
        border-color: #1abc9c;
        outline: 0;
        -webkit-box-shadow: none;
        box-shadow: none;
    }

    /* Navbar */
    .navbar{
        margin-bottom: 0;
        min-height: 30px;
        border-radius: 0;
    }
    .navbar .nav > li{
        float: left; 
    }
    .navbar .nav > li a{
        color: #ffffff;
    }
    .navbar .nav > li a .caret{
        border-bottom-color: #fff;
        border-top-color: #fff;
    }
    .navbar .nav > li a:hover, .navbar .nav > li a:focus, .navbar .nav > li a:active{
        color: #1abc9c;
        background-color: transparent;
    }
    .dropdown-toggle:hover .caret, .dropdown-toggle:focus .caret{
        border-bottom-color: #1abc9c !important;
        border-top-color: #1abc9c !important;
    }
    .nav>li>a, .navbar-brand{
        padding: 0px 15px;
        max-height: 30px;
    }
    .navbar-form{
        padding-bottom: 0;
    }
    .search-query{
        margin-bottom: 7px;
        height: 30px !important;
    }
    .nav a{
        font-size: 15px;
    }
    .navbar-brand{
        font-size: 21px;
    }
    .sidebar-nav{
        box-shadow: inset 0 0 0 rgba(0,0,0,.05);
        padding: 10px;
        background: #95A5A6;
        border-radius: 0;
    }
    .sidebar-nav li a{
        color: #fff;
        display: block;
    }
    .sidebar-nav li:hover, .nav-page-active{
        color: #fff;
        background: #34495E;
        border-left: 4px solid #16a085;
    }
    .sidebar-nav li{
        list-style: none;
        border-bottom: 1px solid #95A5A6;
        padding: 4px;
    }
    .open > .dropdown-menu{
        background-color: #34495e;
        padding: 3px 4px;
    }
    .dropdown-menu{
        border-radius: 4px;
    }
    .dropdown-menu ul{
        min-width: 165px;
        padding-left: 0;
        list-style: none;
    }
    .dropdown-menu li{
        height: 32px;
        padding-top: 3px;
        -webkit-transition: background-color 0.25s;
        transition: background-color 0.25s;
        border-radius: 4px;
    }
    .dropdown-menu li:first-child > a{
        padding-top: 3px;
    }
    .dropdown-menu li a{
        color: #e1e4e7 !important;
        border-radius: 4px;
        padding: 1px 9px;
        font-size: 14px;
        display: block;
    }
    .dropdown-menu li:hover{
        background-color: #1abc9c;
    }
    .dropdown-menu li:hover a{
        color: #ffffff !important;
    }
    .nav-header, .nav-header:hover{
        margin-left: 5px;
        color: #fff;
        background-color: transparent !important;
    }
    .nav > li > a{
        border-right: 1px solid rgb(120, 118, 118);
    }
    .navbar-brand{
        line-height: 1.1em;
    }
    .divider{
        background-color: #2f4154 !important;
        height: 2px;
        margin-left: -4px;
        margin-right: -4px;
    }
    .dropdown.open .dropdown-toggle{
        color: #1abc9c !important;
    }
    .dropdown.open .caret{
        border-bottom-color: #1abc9c !important;
        border-top-color: #1abc9c !important;
    }
    .fui-arrow-right{
        font-size: 12px;
        margin: 0 4px;
    }


    /* Tables */
    .table-bordered{
        border-collapse: separate;
        border-radius: 4px;
    }
    .table-condensed>thead>tr>th{
        padding: 8px;
    }
    table input[type=text]{
        border-radius: 0 !important;
        border: 1px solid #bdc3c7 !important;
        height: 25px !important;
    }
    table thead {
        background: #16A085;
        color: #fff;
    }
    .dataTables_wrapper table{
        margin-left: 13px;
    }

    /* Api Page */
    .swagger-section .swagger-ui-wrap table thead tr th{
        color: #fff !important;
    }
    .swagger-section .swagger-ui-wrap ul#resources li.resource div.heading h2{
        margin: 0;
    }
    .swagger-section .swagger-ui-wrap p{
        font-size: 13px;
    }
    ''')

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
