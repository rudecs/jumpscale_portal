
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

    page.addCSS(cssContent=''' 
    /* General styling */
    .modal{
        position: fixed;
        top: 20%;
        right: 10%;
        bottom: 0;
        left: 0;
        z-index: 1050;
        display: none;
        overflow: hidden;
        -webkit-overflow-scrolling: touch;
        outline: 0;
        max-width: 600px;
        left: 30%;
    }
    .modal-backdrop{
      position: fixed;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      z-index: 1040;
      background-color: #000;
    }
    body{
        font-size: 15px;
        padding-top: 80px !important;
        padding-bottom: 0 !important;
        margin-left: 0;
        margin-top: 0;
    }
    .btn{
        line-height: .9;
    }

    .fixFirefoxSizing{
        transform: none;
        transform-origin: 0;
    }
    .fixFirefoxSizing *, .fixFirefoxSizing .navbar *{
        font-size: 97%;
    }
    .fixFirefoxSizing .search-query{
        margin-bottom: 0;
        height: 25px !important;
    }
    .fixFirefoxSizing .dropdown-menu li{
        max-height: 28px;
    }
    .fixFirefoxSizing select, .fixFirefoxSizing input{
        max-height: 27px;
    }
    .fixFirefoxSizing select{
        border: 1px solid #B1B0B0;
    }
    .fixFirefoxSizing .pagination ul li > a{
        font-size: 13px;
        padding-top: 0;
    }
    .fixFirefoxSizing .pagination ul li.previous > a, .fixFirefoxSizing .pagination ul li.next > a, .fixFirefoxSizing .pagination ul li.previous > span, .fixFirefoxSizing .pagination ul li.next > span{
        padding: 7px 17px;
        height: 32px;
        margin-top: 0;
        margin-right: 0;
        margin-left: 0;
    }
    .fixFirefoxSizing .pagination ul{
        max-height: 33px;
    }
    .fixFirefoxSizing .pagination ul li > a, .pagination ul li > span{
        margin: 5px 2px 6px;
    }
    .fixFirefoxSizing table input[type="text"]{
        max-height: 22px;
    }
    .fixFirefoxSizing .sidebar-nav li{
        padding: 2px;
    }
    .fixFirefoxSizing .container{
        width: 970px;
    }
    .fixFirefoxSizing h1, .h1{
        font-size: 34px;
    }
    .fixFirefoxSizing h2, .h2{
        font-size: 29px;
    }
    .fixFirefoxSizing h3, .h3{
        font-size: 24px;
    }
    .fixFirefoxSizing h4, .h4{
        font-size: 19px;
    }
    .fixFirefoxSizing h5, .h5{
        font-size: 18px;
    }
    .fixFirefoxSizing h6, .h6{
        font-size: 17px;
    }
    .fixFirefoxSizing .table-condensed > thead > tr > th{
        padding: 6px;
    }
    .fixFirefoxSizing .navbar-brand{
        line-height: 0.9em;
    }
    body.fixFirefoxSizing input[type="text"]{
        font-size: 13px;
    }
    .fixFirefoxSizing .sidebar-nav li a, .fixFirefoxSizing .sidebar-nav a{
        font-size: 13px;
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
    .fixFirefoxSizing .navbar-brand, .navbar-brand{
        font-size: 21px;
    }
    .sidebar-nav{
        box-shadow: inset 0 0 0 rgba(0,0,0,.05);
        padding: 10px;
        background: #95A5A6;
        border-radius: 0;
    }
    .sidebar-nav li a, .sidebar-nav a{
        color: #fff;
        display: block;
        font-size: 15px;
    }
    .sidebar-nav li:hover, .nav-page-active, .sidebar-nav p:hover{
        color: #fff;
        background: #34495E;
        border-left: 4px solid #16a085;
    }
    .sidebar-nav li, .sidebar-nav p{
        list-style: none;
        border-bottom: 1px solid #95A5A6;
        padding: 4px;
    }
    .sidebar-nav p{
        margin-bottom: 0;
        padding: 2px;
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
    .fixFirefoxSizing .dropdown-menu li a{
        font-size: 12px;
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

    /* Breadcrumb */
    .fixFirefoxSizing .fui-arrow-right, .fui-arrow-right{
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
    .dataTables_wrapper table.table thead .sorting_asc{
        background: url('/jslib/old/datatables/images/white-theme/sort_asc.png') no-repeat center right;
    }
    .dataTables_wrapper table.table thead .sorting_desc{
        background: url('/jslib/old/datatables/images/white-theme/sort_desc.png') no-repeat center right;
    }
    div.dataTables_length select{
        border-radius: 4px;
        height: 35px;
    }
    .pagination ul li > a, .pagination ul li > span, .pagination ul li.active > a:hover{
        color: #34495e;
    }
    .pagination ul li > a:hover, .pagination ul li > span:hover{
        color: #fff;
    }
    .previous.disabled a:hover, .next.disabled a:hover, .previous.disabled a:focus, .next.disabled a:focus, .previous.disabled a:active, .next.disabled a:active{
        background: #d6dbdf;
        color: #34495e;
        cursor: default;
    }
    .flatTheme .dataTables_wrapper.form-inline{
        width: 100%;
    }

    /* Api Page */
    .swagger-section .swagger-ui-wrap table thead tr th{
        color: #fff !important;
    }
    .swagger-section .swagger-ui-wrap ul#resources li.resource div.heading h2{
        margin: 0;
    }
    .fixFirefoxSizing .swagger-section .swagger-ui-wrap p, .swagger-section .swagger-ui-wrap p{
        font-size: 13px;
    }

    /* Explorer Page */
    .elfinder .elfinder-button{
        width: 25px !important;
    }

    /* Edit Page */
    .cm-s-monokai.CodeMirror{
        background: #34495e !important;
        min-height: 300px;
    }

    ''')

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
