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
            
            array_container: function(context) {
                return $(context).parents('.array').first();
            },
            
            array_template: function(context) {
                var array_container = yafowil.array.array_container(context);
                var tmpl = array_container.children('.arraytemplate').clone();
                return tmpl;
            },
            
            create_row: function(context) {
                var row = '';
                row += '<tr>';
                row +=   '<td class="widget">';
                row +=   '</td>';
                row +=   '<td class="actions">';
                row +=     '<div class="array_actions">';
                row +=       '<a class="array_row_add" href="#">&nbsp;</a>';
                row +=       '<a class="array_row_remove" href="#">&nbsp</a>';
                row +=       '<a class="array_row_up" href="#">&nbsp</a>';
                row +=       '<a class="array_row_down" href="#">&nbsp</a>';
                row +=     '</div>';
                row +=   '</td>';
                row += '</tr>';
                row = $(row);
                var template = yafowil.array.array_template(context);
                $('.widget', row).append(template.children());
                return row;
            },
            
            get_row: function(action) {
                return $(action).parent().parent().parent();
            },
            
            base_id: function(context) {
                var id = context.parents('.array').first().attr('id');
                return id.substring(6, id.length);
            },
            
            reset_indices: function(context) {
                var index = 0;
                var container = yafowil.array.array_container(context);
                var base_id = yafowil.array.base_id(context);
                context.children().each(function() {
                    yafowil.array.set_row_index(base_id, this, index++);
                });
                yafowil.array.binder(context);
            },
            
            set_row_index: function(base_id, row, index) {
                yafowil.array.recursiv_set_row_index(row, base_id, index);
            },
            
            recursiv_set_row_index: function(node, base_id, index) {
                var base_name = base_id.replace(/\-/g, '.');
                var set_index = yafowil.array.set_attr_index;
                var child, id, name, for_;
                $(node).children().each(function() {
                    child = $(this);
                    set_index(child, 'id', base_id, index, '-');
                    set_index(child, 'for', base_id, index, '-');
                    set_index(child, 'name', base_name, index, '.');
                    yafowil.array.recursiv_set_row_index(
                        child, base_id, index);
                });
            },
            
            set_attr_index: function(node, attr, base, index, delim) {
                var value = node.attr(attr);
                if (value && value.indexOf(base) > -1) {
                    var idx_0 = value.indexOf(base) + base.length + 1;
                    var idx_1 = value.indexOf(delim, idx_0);
                    var pre = value.substring(0, idx_0);
                    var post = '';
                    if (idx_1 > -1) {
                        var post = value.substring(idx_1, value.length);
                    }
                    node.attr(attr, pre + index + post);
                }
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
                        var new_row = yafowil.array.create_row(this);
                        var container = row.parent();
                        if (container.get(0).tagName.toLowerCase() == 'tbody') {
                            row.after(new_row);
                        } else {
                            var table = container.parent();
                            var body = $('tbody', table).first();
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
