/* jslint browser: true */
/* global jQuery, yafowil */
/*
 * yafowil array widget
 */

if (window.yafowil === undefined) {
    window.yafowil = {};
}

(function($, yafowil) {
    "use strict";

    $(document).ready(function() {
        // initial binding
        yafowil.array.binder(document);
        
        // add after ajax binding if bdajax present
        if (window.bdajax !== undefined) {
            window.bdajax.register(yafowil.array.binder.bind(yafowil.array));
        }
    });

    $.extend(yafowil, {

        array: {

            hooks: {
                before_add: {},
                add: {},
                remove: {},
                before_up: {},
                up: {},
                before_down: {},
                down: {},
                index: {}
            },

            container: function(context) {
                return $(context).parents('.array').first();
            },

            template: function(context) {
                var container = this.container(context);
                var tmpl = container.children('.arraytemplate').clone();
                return tmpl;
            },

            create_row: function(context) {
                var css = $(context).parents('.array').attr('class');
                var row = '';
                row +=   '<tr>';
                row +=     '<td class="widget">';
                row +=     '</td>';
                if (css.indexOf('array-static') === -1) {
                    row += '<td class="actions">';
                    row +=   '<div class="array_actions">';
                    if (css.indexOf('array-add') > -1) {
                        row += '<a class="array_row_add" href="#">';
                        row +=   '<span class="icon-plus-sign"> </span>';
                        row += '</a>';
                    }
                    if (css.indexOf('array-remove') > -1) {
                        row += '<a class="array_row_remove" href="#">';
                        row +=   '<span class="icon-minus-sign"> </span>';
                        row += '</a>';
                    }
                    if (css.indexOf('array-sort') > -1) {
                        row += '<a class="array_row_up" href="#">';
                        row +=   '<span class="icon-circle-arrow-up"> </span>';
                        row += '</a>';
                        row += '<a class="array_row_down" href="#">';
                        row +=   '<span class="icon-circle-arrow-down"> </span>';
                        row += '</a>';
                    }
                    row +=   '</div>';
                    row += '</td>';
                }
                row +=   '</tr>';
                row = $(row);
                var template = this.template(context);
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
                var base_id = this.base_id(context);
                var that = this;
                var row;
                context.children().each(function() {
                    row = $(this);
                    that.set_row_index(row, base_id, index);
                    that.notify_hooks(that.hooks.index, row, index);
                    index++;
                });
                this.binder(context);
            },

            set_row_index: function(node, base_id, index) {
                var base_name = base_id.replace(/\-/g, '.');
                var set_index = this.set_attr_index.bind(this);
                var that = this;
                var child;
                node.children().each(function() {
                    child = $(this);
                    set_index(child, 'id', base_id, index, '-');
                    set_index(child, 'for', base_id, index, '-');
                    set_index(child, 'name', base_name, index, '.');
                    that.set_row_index(child, base_id, index);
                });
            },

            set_attr_index: function(node, attr, base, index, delim) {
                var value = node.attr(attr);
                if (value && value.indexOf(base) > -1) {
                    node.attr(
                        attr,
                        this.set_value_index(value, base, index, delim)
                    );
                }
            },

            set_value_index: function(value, base, index, delim) {
                var idx_0 = value.indexOf(base) + base.length + 1;
                var idx_1 = value.indexOf(delim, idx_0);
                var pre = value.substring(0, idx_0);
                var post = '';
                if (idx_1 > -1) {
                    post = value.substring(idx_1, value.length);
                }
                return pre + index + post;
            },

            mark_disabled: function(context) {
                if (context !== document) {
                    context = $(context).parent();
                } else {
                    context = $(context);
                }
                var up_sel = '> tr > td.actions a.array_row_up';
                var down_sel = '> tr > td.actions a.array_row_down';
                $('tbody:visible', context).each(function() {
                    var body = $(this);
                    $(up_sel, body)
                        .removeClass('array_row_up_disabled')
                        .first()
                        .addClass('array_row_up_disabled');
                    $(down_sel, body)
                        .removeClass('array_row_down_disabled')
                        .last()
                        .addClass('array_row_down_disabled');
                });
            },

            notify_hooks: function(hooks, ...args) {
                for (var name in hooks) {
                    hooks[name].apply(null, args);
                }
            },

            array_row_add: function(event) {
                event.preventDefault();
                var row = this.get_row(event.currentTarget);
                var new_row = this.create_row(event.currentTarget);
                var container = row.parent();
                if (container.get(0).tagName.toLowerCase() === 'tbody') {
                    this.notify_hooks(this.hooks.before_add, new_row, container);
                    row.after(new_row);
                } else {
                    var table = container.parent();
                    var body = $('tbody', table).first();
                    container = body;
                    this.notify_hooks(this.hooks.before_add, new_row, container);
                    container.prepend(new_row);
                }
                this.reset_indices(container);
                this.notify_hooks(this.hooks.add, new_row);
            },

            array_row_remove: function(event) {
                event.preventDefault();
                var row = this.get_row(event.currentTarget);
                this.notify_hooks(this.hooks.remove, row);
                var container = row.parent();
                row.remove();
                this.reset_indices(container);
            },

            array_row_up: function(event) {
                event.preventDefault();
                var row = this.get_row(event.currentTarget);
                this.notify_hooks(this.hooks.before_up, row);
                row.insertBefore(row.prev());
                this.reset_indices(row.parent());
                this.notify_hooks(this.hooks.up, row);
            },

            array_row_down: function(event) {
                event.preventDefault();
                var row = this.get_row(event.currentTarget);
                this.notify_hooks(this.hooks.before_down, row);
                row.insertAfter(row.next());
                this.reset_indices(row.parent());
                this.notify_hooks(this.hooks.down, row);
            },

            binder: function(context) {
                this.mark_disabled(context);
                var add_sel = 'a.array_row_add';
                var add_handler = this.array_row_add.bind(this)
                $(add_sel, context).off().on('click', add_handler);
                var remove_sel = 'a.array_row_remove';
                var remove_handler = this.array_row_remove.bind(this);
                $(remove_sel, context).off().on('click', remove_handler);
                var up_sel = 'a.array_row_up';
                var up_handler = this.array_row_up.bind(this)
                $(up_sel, context).off().on('click', up_handler);
                var down_sel = 'a.array_row_down';
                var down_handler = this.array_row_down.bind(this)
                $(down_sel, context).off().on('click', down_handler);
            }
        }
    });

})(jQuery, yafowil);
