
def main(j, args, params, tags, tasklet):

    page = args.page
    params.extend(args)
    page.addHTMLHeader('''<link rel="shortcut icon" type="image/png" href="/system/.files/img/favicon.png">''')
    page.addCSS('/jslib/bootstrap/css/bootstrap-3-3-1.min.css')
    page.addCSS('/jslib/flatui/css/flat-ui.css')
    page.addCSS('/jslib/new-ui/new-ui.css')
    page.addCSS('/jslib/new-ui/oocss.css')

    page.addJS('/jslib/jquery/jquery-2.0.3.min.js')
    page.addJS('/jslib/jquery/jquery-migrate-1.2.1.js')
    page.addJS('/jslib/old/jquery.cookie.js')
    page.addJS('/jslib/bootstrap/js/bootstrap-3-3-2.min.js')


    page.addJS('/jslib/pnotify/pnotify.js')
    page.addJS('/jslib/pnotify/pnotify.buttons.js')
    page.addCSS('/jslib/pnotify/pnotify.css')

    page.addJS(jsContent='''
        $( function () {
        $('body').addClass('flatTheme');

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

        var toggles = document.querySelectorAll(".c-hamburger");
        for (var i = toggles.length - 1; i >= 0; i--) {
            var toggle = toggles[i];
            toggleHandler(toggle);
        };
        function toggleHandler(toggle) {
            toggle.addEventListener( "click", function(e) {
              e.preventDefault();
              (this.classList.contains("is-active") === true) ? this.classList.remove("is-active") : this.classList.add("is-active");
              $('.page-content').find('.sidebar-nav').toggleClass('hide');
              $('.page-content').find('.content').toggleClass('less-wide');
              $('.page-content').find('.navigation').toggleClass('wide-sidebar');
            });
        }

        //pnotify stuff
        PNotify.prototype.options.styling = "bootstrap3";
        var eventId = sessionStorage.getItem('event.id');
        if (eventId == null) {
            eventId = Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
            sessionStorage.setItem('event.id', eventId);
        }
        var notifications = {};
        var getevents = function() {
            $.ajax({url: '/restmachine/system/contentmanager/checkEvents',
                    data: {
                        key: eventId
                    },
                    success: function(data) {
                        if (data) {
                            data.buttons = {sticker: false};
                            if (data.refresh_hint && data.refresh_hint == location) {
                                data.hide = false;
                                data.text += "<a href='javascript:window.reloadAll()'> refresh page</a>"
                            }
                            if (data.title in notifications) {
                                var notify = notifications[data.title];
                                notify.update(data);
                            } else {
                                var notify = new PNotify(data);
                            }
                            if (data.type == 'info') {
                                notifications[data.title] = notify;
                            } else {
                                delete notifications[data.title];
                            }
                        }
                        setTimeout(getevents, 0);
                    },
                    error: function(data) {
                        console.log('Failed to call checkEvents');
                        setTimeout(getevents, 3000);
                    }
            });

        };
        setTimeout(getevents, 0);

    });
     ''')

    page.removeJS('/jslib/old/jquery-latest.js')
    page.removeJS('/jslib/old/bootstrap/js/bootstrap.js')
    page.removeJS('/jslib/old/jquery.cookie.js')

    page.addCSS('/system/.files/css/flatTheme.css')

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
