var eveModule = angular.module('eveModule', []);
eveModule.directive('eveGrid', function($http, $filter) {
    return {
        restrict: 'EA',
        scope: true,
        template:'<div id="spin"></div><table style="margin-top: 10px;" class="table table-striped dataTable table-bordered" cellspacing="0" width="100%"><tfoot><tr><td><button class="delete btn btn-danger" style="padding: 2px 12px;">Delete</button></td></tr></tfoot></table>',
        link: function (scope, element, attrs, ctrl) {
            angular.element(".navbar").find(".nav").find(".dropdown").on( "click", function() {
              angular.element( this ).toggleClass( "open" );
            });
            if(attrs['eveUrl'][0] == ":" ){
                attrs['eveUrl'] = window.location.protocol + "//" + window.location.hostname + attrs['eveUrl'];
            } else if (attrs['eveUrl'][0] == "/") {
                attrs['eveUrl'] = window.location.protocol + "//" + window.location.host + attrs['eveUrl'];
            }
            var checkedRows = [];
            var publicRequestData= [];
            var searchInputChanged = false;
            var opts = {
              lines: 9,
              length: 6,
              width: 3,
              radius: 4,
              corners: 0.5,
              rotate: 0,
              direction: 1,
              color: '#000',
              speed: 1.1,
              trail: 87,
              shadow: false,
              hwaccel: false,
              className: 'spinner',
              zIndex: 2e9,
              top: '2%',
              left: '50%'
            };

            var target = document.getElementById('spin');
            var spinner = new Spinner(opts).spin(target);
            $http({
                url: attrs['eveUrl'] + attrs['eveSpecPath'],
                method: 'GET',

            }).then(function(data) {
                scope.schema = data.data;
                var columns = [{
                    data: null,
                    orderable: false,
                    defaultContent: '<input class="rowCheck" type="checkbox"></input>',
                    'title': '<input class="allCheck" type="checkbox"></input>'
                }];
                var showFields = [];
                var eveFields = scope.schema.domains[attrs["eveEntity"]]['/' + attrs["eveEntity"]].POST.params;

                for (var i = 0; i < JSON.parse( attrs['columns'] ).length; i++) {
                    var field = _.findWhere(eveFields, {name: JSON.parse( attrs['columns'] )[i].data});
                    if(field){
                        field.header = JSON.parse( attrs['columns'] )[i].header;
                        field.format = JSON.parse( attrs['columns'] )[i].format;
                        showFields.push(field);
                    }
                };
                columns = columns.concat(showFields
                    .filter(function(p) { return p.name.indexOf('.') == -1; })
                    .map(function(param, mapIndex) {
                        var column = {};
                        column.data = param.name;
                        column.title = param.header;
                        column.class = "details-control";
                        column.defaultContent = '';
                        column.type = param.type;
                        column.render = function(data, type, row) {
                            var columnText = data;

                            var datetimeFields = attrs["datetimeFields"].split(',');
                            if( datetimeFields.indexOf(column.data) > -1 ){
                                column.type = "datetime";
                                columnText = new Date(data * 1000).toLocaleString();
                            }
                            if(param.format){
                                columnText = param.format.replace(RegExp('{' + column.data + '}', 'g'), columnText);
                                for (var i = 0; i < scope.columns.length; i++) {
                                    columnText = columnText.replace(RegExp('{' + scope.columns[i].data + '}', 'g'), row[scope.columns[i].data]);
                                    if( columnText.indexOf("{") > -1 ){
                                        var fullFormat = columnText.match(/{(.*)}/);
                                        if (fullFormat != null){
                                            var fieldToFormat = fullFormat[0].replace(/{(.*)}/, '$1');
                                        }
                                        var field = _.findWhere(eveFields, {name: fieldToFormat});
                                        columnText = columnText.replace(RegExp('{' + field.name + '}', 'g'), row[field.name]);
                                    }
                                };
                            }
                            if( column.type == "string"){
                                columnText = jQuery('<span>').text(columnText).attr('title', columnText)[0].outerHTML;
                            }
                            return columnText;
                        },
                        column.getFilter = function(val, val2) {
                            if (val && val.length > 0 && column.type == 'string')
                                return '"' + column.data + '":{"$regex":"' + val + '", "$options": "i"}';
                            else if (column.type == 'date' || column.type == 'datetime') {
                                var predicate = [];
                                if (val && val.length > 0) {
                                    val = moment(val, 'DD/MM/YYYY hh:mm:ss').format('X');
                                    predicate.push('"$gte":' + val);
                                }
                                if (val2 && val2.length > 0) {
                                    val2 = moment(val2, 'DD/MM/YYYY hh:mm:ss').format('X');
                                    predicate.push('"$lte":' + val2);
                                }

                                if (predicate.length == 0)
                                    return '';
                                return '"' + column.data + '":' + '{' + predicate.join(', ') + '}';
                            }
                            else if (column.type == 'integer' || column.type == 'float'){
                                var predicate = [];
                                if (val && val.length > 0)
                                    predicate.push('"$gte":' + val);
                                if (val2 && val2.length > 0)
                                    predicate.push('"$lte":' + val2);

                                if (predicate.length == 0)
                                    return '';
                                return '"' + column.data + '":' + '{' + predicate.join(', ') + '}';
                            }
                            else
                                return '';

                        }
                        return column;
                    }));
                scope.columns = columns;
                scope.dataTable = angular.element('#' + attrs["eveEntity"] + '-container table').DataTable( {
                    processing: true,
                    serverSide: true,
                    "columnDefs": [
                        { className: "center", "targets": [ 0 ] }
                    ],
                    "columns": scope.columns,
                    ajax: function(requestData, callback, settings) {
                        requestData.page = requestData.start / requestData.length + 1;
                        requestData.max_results = requestData.length;
                        if( angular.element('#' + attrs["eveEntity"] + '-container table').find('.allCheck').is(':checked') ){
                            setTimeout(function() {
                                for (var i = 0; i < angular.element('#' + attrs["eveEntity"] + '-container table').find('.rowCheck').length; i++) {
                                    if(angular.element('#' + attrs["eveEntity"] + '-container table').find('.rowCheck').eq(i).is(':checked') == false ){
                                        angular.element('#' + attrs["eveEntity"] + '-container table').find('.rowCheck').eq(i).prop('checked', true).parents('tr').addClass('selected');
                                    }
                                };
                            }, 200);
                        }
                        var where = [];
                        for (var i = 1; i < scope.columns.length; i++){
                            var val = angular.element( '#' + attrs["eveEntity"] + '-container table tfoot td:eq(' + i + ') input:first' ).val();
                            var val2 = angular.element( '#' + attrs["eveEntity"] + '-container table tfoot td:eq(' + i + ') input:nth(1)' ).val();
                            where.push(scope.columns[i].getFilter(val, val2));
                        };
                        if(requestData.order && requestData.order.length > 0) {
                            sort_field = scope.columns[requestData.order[0].column].data;
                            sort_dir = requestData.order[0].dir == 'desc' ? -1 : 1
                            requestData.sort = '[("' + sort_field + '",' + sort_dir + ')]';
                        }
                        if(requestData.sort.indexOf('null') > -1){
                            requestData.sort = attrs['sortby'];
                        }
                        var whereStatment = [];
                        for (var i = 0; i < where.length; i++) {
                            if(where[i].length > 0){
                                whereStatment.push(where[i]);
                            }
                        };
                        if (whereStatment.length > 0){
                            whereStatment.length = 0;
                            requestData.where = "{" + where.filter(function(s) {return s.length > 0; }).join(', ') + "}";
                            var target = document.getElementById('spin');
                            var spinner = new Spinner(opts).spin(target);
                            $http({
                                url: attrs['eveUrl'] + '/' + attrs["eveEntity"],
                                method: 'GET',
                                cache: false,
                                params: requestData
                            }).then(function(data) {
                                data = data.data;
                                if (data['_meta']) {
                                    data['recordsTotal'] = data['_meta']['total'];
                                    data['iTotalRecords'] = data['_meta']['total'];
                                    data['iTotalDisplayRecords'] = data['_meta']['total'];
                                } else {
                                    data['recordsTotal'] = 0;
                                    data['iTotalRecords'] = 0;
                                    data['iTotalDisplayRecords'] = 0;
                                }
                                data['data'] = data['_items'];
                                callback(data);
                                spinner.stop();
                            }, function (argument) {
                                spinner.stop();
                            });
                        }else{
                            var target = document.getElementById('spin');
                            var spinner = new Spinner(opts).spin(target);
                            $http({
                                url: attrs['eveUrl'] + '/' + attrs["eveEntity"],
                                method: 'GET',
                                cache: false,
                                params: requestData
                            }).then(function(data) {
                                data = data.data;
                                if (data['_meta']) {
                                    data['recordsTotal'] = data['_meta']['total'];
                                    data['iTotalRecords'] = data['_meta']['total'];
                                    data['iTotalDisplayRecords'] = data['_meta']['total'];
                                } else {
                                    data['recordsTotal'] = 0;
                                    data['iTotalRecords'] = 0;
                                    data['iTotalDisplayRecords'] = 0;
                                }
                                data['data'] = data['_items'];
                                callback(data);
                                spinner.stop();
                            });
                        }
                        publicRequestData = requestData;
                    },
                } );
                for (var i = 1; i < scope.columns.length; i++) {
                    var datetimeFields = attrs["datetimeFields"].split(',');
                    if(scope.columns[i].sType == "integer" || scope.columns[i].sType == "float"){
                        if( datetimeFields.indexOf(scope.columns[i].data) > -1 ){
                            angular.element('<td style="padding-left: 0;">' +
                                '<input type="text" class="searchInput datetimeInput" placeholder=">=" data-date-format="DD/MM/YYYY hh:mm:ss"/>' +
                                '<input type="text" class="searchInput datetimeInput" placeholder="<=" data-date-format="DD/MM/YYYY hh:mm:ss"/>' +
                                '</td>')
                                .appendTo('#' + attrs["eveEntity"] + '-container table tfoot tr')
                                .on( 'keyup change', function () {
                                    scope.dataTable
                                        .column( i )
                                        // .search( angular.element(this).find('input').val() )
                                        .draw();
                                } );
                        }else{
                            angular.element('<td style="padding-left: 0;">' +
                                '<input type="text" class="searchInput" placeholder=">=" />' +
                                '<input type="text" class="searchInput" placeholder="<=" />' +
                                '</td>')
                                .appendTo('#' + attrs["eveEntity"] + '-container table tfoot tr')
                                .on( 'keyup change', function () {
                                    scope.dataTable
                                        .column( i )
                                        // .search( angular.element(this).find('input').val() )
                                        .draw();
                                } );
                        }
                    }
                    else{
                        angular.element('<td style="padding-left: 0;"><input type="text" class="searchInput" /></td>')
                            .appendTo('#' + attrs["eveEntity"] + '-container table tfoot tr')
                            .on( 'keyup change', function () {
                                scope.dataTable
                                    .column( i )
                                    .search( angular.element(this).find('input').val() )
                                    .draw();
                            } );
                    }
                };

                $('.searchInput').each(function() {

                    var elem = $(this);
                    elem.data( 'oldVal', elem.val() );
                    elem.live("keyup paste", function(event){
                        if (elem.data('oldVal') != elem.val()) {
                            angular.element('#' + attrs["eveEntity"] + '-container table').find('.allCheck').prop('checked', false);
                            searchInputChanged = true;
                            elem.data('oldVal', elem.val());
                        }else{
                            searchInputChanged = false;
                        }
                    });

                });
                $('.datetimeInput').datetimepicker();
                angular.element('.eve-grid-container .rowCheck').live('click' , function() {
                    var currentRow = $(this).parents('tr');
                    $(currentRow).toggleClass('selected');
                });
                spinner.stop();
            });
            angular.element('#' + attrs["eveEntity"] + '-container table').on('click', '.allCheck', function() {
                var allCheck = this;
                if (allCheck.checked){
                    setTimeout(function() {
                        angular.element('.rowCheck').prop('checked', true).parents('tr').addClass('selected');
                    }, 100);
                }else{
                    setTimeout(function() {
                        angular.element('.rowCheck').prop('checked', false).parents('tr').removeClass('selected');
                    }, 100);
                }
            });
            angular.element('.searchInput').live('focus', function() {
                $(this).animate({ width: 116 }, 'medium');
            }).live('blur', function() {
                $(this).animate({ width: 60 }, 'medium');
            });
            angular.element('#' + attrs["eveEntity"] + '-container table .delete').on('click', function() {
                if(scope.dataTable.rows('.selected').data().length > 0){
                    $("#confirmModal").modal('show');
                }
            });
            angular.element('.eve-grid-container .confirmDelete').on('click', function() {
                $http({
                    url: attrs['eveUrl'] + '/' + attrs["eveEntity"],
                    method: 'GET',
                    cache: false,
                    params: publicRequestData
                }).then(function(data) {
                    data = data.data;
                    data['data'] = data['_items'];
                    publicRequestData.length = data._meta.total;
                    publicRequestData.max_results = data._meta.total;
                    publicRequestData.page = "";
                    $http({
                        url: attrs['eveUrl'] + '/' + attrs["eveEntity"],
                        method: 'GET',
                        cache: false,
                        params: publicRequestData
                    }).then(function(data) {
                        data = data.data;
                        if (data['_meta']) {
                            data['recordsTotal'] = data['_meta']['total'];
                            data['iTotalRecords'] = data['_meta']['total'];
                            data['iTotalDisplayRecords'] = data['_meta']['total'];
                        } else {
                            data['recordsTotal'] = 0;
                            data['iTotalRecords'] = 0;
                            data['iTotalDisplayRecords'] = 0;
                        }
                        publicRequestData.length = 0;
                        var rows = scope.dataTable.rows('.selected').data();
                        if(rows.length > 0){
                             for (var i = 0; i < rows.length; i++) {
                                var row = rows[i];
                                 $http({
                                      url: attrs['eveUrl'] + '/' + attrs["eveEntity"] + '/'+ row._id,
                                      type: 'POST',
                                      headers: {
                                          'X-HTTP-Method-Override': 'DELETE',
                                          'If-Match': row._etag
                                      }
                                 }).then(function() {
                                    scope.dataTable.draw();

                                 });
                             };
                        }
                    });
                    angular.element('#' + attrs["eveEntity"] + '-container table').find('.allCheck').prop('checked', false);
                });
                $("#confirmModal").modal('hide');
            });
        }
    }
});
