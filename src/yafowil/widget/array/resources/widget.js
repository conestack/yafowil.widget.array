/*
 * yafowil array widget
 */

if (typeof(window['yafowil']) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        // initial binding
        yafowil.array.binder();
        
        // add after ajax binding if bdajax present
        if (typeof(window['bdajax']) != "undefined") {
            $.extend(bdajax.binders, {
                arraywidget_binder: yafowil.array.binder
            });
        }
    });
    
    $.extend(yafowil, {
        
        array: {
            
            create_row: function() {
                var row = '';
                row += '<tr>';
                row +=   '<td class="key">';
                row +=     '<input type="text" value="" />';
                row +=   '</td>';
                row +=   '<td class="value">';
                row +=     '<input type="text" value="" />';
                row +=   '</td>';
                row +=   '<td>';
                row +=     '<div class="array_actions">';
                row +=       '<a class="array_row_add" href="#">&nbsp;</a>';
                row +=       '<a class="array_row_remove" href="#">&nbsp</a>';
                row +=       '<a class="array_row_up" href="#">&nbsp</a>';
                row +=       '<a class="array_row_down" href="#">&nbsp</a>';
                row +=     '</div>';
                row +=   '</td>';
                row += '</tr>';
                return row;
            },
            
            get_row: function(action) {
                return $(action).parent().parent().parent();
            },
            
            base_name: function(context) {
                return context.parents('.arraywidget').attr('id');
            },
            
            reset_indices: function(context) {
                var index = 0;
                var base_name = yafowil.array.base_name(context);
                base_name = base_name.substring(11, base_name.length);
                var base_id = base_name.replace(/\./g, '-');
                $('tr', context).each(function() {
                    row = $(this);
                    key = $('td.key input', row);
                    key_id = base_id + index + '-key';
                    key_name = base_name + index + '.key';
                    key.attr('id', key_id).attr('name', key_name);
                    value = $('td.value input', row);
                    value_id = base_id + index + '-value';
                    value_name = base_name + index + '.value';
                    value.attr('id', value_id).attr('name', value_name);
                    index++;
                });
                yafowil.array.binder(context);
            },
            
            mark_disabled: function(context) {
                context = $(context);
                $('a.array_row_up', context)
                    .removeClass('array_row_up_disabled')
                    .first()
                    .addClass('array_row_up_disabled');
                $('a.array_row_down', context)
                    .removeClass('array_row_down_disabled')
                    .last()
                    .addClass('array_row_down_disabled');
            },
            
            binder: function(context) {
                yafowil.array.mark_disabled(context);
                $('a.array_row_add', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.array.get_row(this);
                        var new_row = yafowil.array.create_row();
                        var container = row.parent();
                        if (container.get(0).tagName.toLowerCase() == 'tbody') {
                            row.after(new_row);
                        } else {
                            var table = container.parent();
                            var body = $('tbody', table);
                            // jq 1.4.4 fails atm
                            //if (!body.length) {
                            //    body = $('<tbody />');
                            //    table.append(body);
                            //}
                            container = body;
                            container.prepend(new_row);
                        }
                        yafowil.array.reset_indices(container);
                    });
                
                $('a.array_row_remove', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.array.get_row(this);
                        var container = row.parent();
                        row.remove();
                        yafowil.array.reset_indices(container);
                    });
                
                $('a.array_row_up', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.array.get_row(this);
                        row.insertBefore(row.prev());
                        yafowil.array.reset_indices(row.parent());
                    });
                
                $('a.array_row_down', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.array.get_row(this);
                        row.insertAfter(row.next());
                        yafowil.array.reset_indices(row.parent());
                    });
            }
        }
    });

})(jQuery);