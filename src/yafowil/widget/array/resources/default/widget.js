var yafowil_array = (function (exports, $) {
    'use strict';

    function escape_regexp(value) {
        return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    class ArrayBase {
        constructor(wrapper) {
            wrapper.data('yafowil-array', this);
            this.wrapper = wrapper;
            const table = $('> table', wrapper),
                head_actions = $('> thead .array_actions', table),
                add_handle = this.add_first_handle.bind(this);
            this.table = table;
            $('a.array_row_add', head_actions).off().on('click', add_handle);
            this.bind_actions();
        }
        bind_actions() {
            const actions_sel = '> tbody > tr > td.actions .array_actions',
                row_actions = $(actions_sel, this.table),
                add_handle = this.add_handle.bind(this),
                remove_handle = this.remove_handle.bind(this),
                up_handle = this.up_handle.bind(this),
                down_handle = this.down_handle.bind(this);
            this.mark_disabled(row_actions);
            $('a.array_row_add', row_actions).off().on('click', add_handle);
            $('a.array_row_remove', row_actions).off().on('click', remove_handle);
            $('a.array_row_up', row_actions).off().on('click', up_handle);
            $('a.array_row_down', row_actions).off().on('click', down_handle);
        }
        mark_disabled(row_actions) {
            $('a.array_row_up', row_actions)
                .removeClass('array_row_up_disabled')
                .first()
                .addClass('array_row_up_disabled');
            $('a.array_row_down', row_actions)
                .removeClass('array_row_down_disabled')
                .last()
                .addClass('array_row_down_disabled');
        }
        create_row() {
            const css = this.wrapper.attr('class');
            let row = '';
            row += '<tr>';
            row += '<td class="widget">';
            row += '</td>';
            if (css.indexOf('array-static') === -1) {
                row += '<td class="actions">';
                row += '<div class="array_actions">';
                if (css.indexOf('array-add') > -1) {
                    row += '<a class="array_row_add" href="#">';
                    row += `<span class="${this.icon_add}"> </span>`;
                    row += '</a>';
                }
                if (css.indexOf('array-remove') > -1) {
                    row += '<a class="array_row_remove" href="#">';
                    row += `<span class="${this.icon_remove}"> </span>`;
                    row += '</a>';
                }
                if (css.indexOf('array-sort') > -1) {
                    row += '<a class="array_row_up" href="#">';
                    row += `<span class="${this.icon_up}"> </span>`;
                    row += '</a>';
                    row += '<a class="array_row_down" href="#">';
                    row += `<span class="${this.icon_down}"> </span>`;
                    row += '</a>';
                }
                row += '</div>';
                row += '</td>';
            }
            row += '</tr>';
            row = $(row);
            const template = $('> .arraytemplate', this.wrapper).clone();
            $('.widget', row).append(template.children());
            return row;
        }
        get_row(action) {
            return $(action).parent().parent().parent();
        }
        get base_id() {
            const id = this.wrapper.attr('id');
            return id.substring(6, id.length);
        }
        trigger(event, ...args) {
            const event_hooks = this.hooks[event.substring(3, event.length)];
            if (Object.entries(event_hooks).length) {
                console.log('Array hooks are deprecated. Use ``on_array_event`` instead.');
                for (const hook_name in event_hooks) {
                    console.log(`    - ${hook_name}`);
                    event_hooks[hook_name].apply(null, args);
                }
            }
            args.splice(0, 0, this);
            for (const subscriber of this._array_subscribers[event]) {
                subscriber.apply(null, args);
            }
        }
        reset_indices(context) {
            let index = 0,
                base_id = this.base_id,
                that = this,
                row;
            context.children().each(function () {
                row = $(this);
                that.set_row_index(row, base_id, index);
                that.trigger('on_index', row, index);
                index++;
            });
            this.bind_actions();
        }
        set_row_index(node, base_id, index) {
            let base_name = base_id.replace(/-/g, '.'),
                set_index = this.set_attr_index.bind(this),
                that = this,
                child;
            node.children().each(function () {
                child = $(this);
                for (const attr of ['id', 'for']) {
                    set_index(child, attr, base_id, index, '-');
                    set_index(child, attr, base_name, index, '.');
                }
                set_index(child, 'name', base_name, index, '.');
                that.set_row_index(child, base_id, index);
            });
        }
        set_attr_index(node, attr, base, index, delim) {
            const value = node.attr(attr);
            if (value && value.indexOf(base) > -1) {
                node.attr(attr, this.set_value_index(value, base, index, delim));
            }
        }
        set_value_index(value, base, index, delim) {
            const pattern = new RegExp(
                `((?:^|[-._])${escape_regexp(base + delim)})(?:\\d+|TEMPLATE)(?=[-.]|$)`,
            );
            return value.replace(pattern, (_match, head) => head + index);
        }
        init_row(container, row) {
            this.reset_indices(container);
            this.array_widget.initialize(row);
            this.trigger('on_add', row);
        }
        add_first_handle(evt) {
            evt.preventDefault();
            const new_row = this.create_row(),
                container = $('> tbody', this.table);
            this.trigger('on_before_add', new_row, container);
            container.prepend(new_row);
            this.init_row(container, new_row);
        }
        add_handle(evt) {
            evt.preventDefault();
            const row = this.get_row(evt.currentTarget),
                new_row = this.create_row(),
                container = row.parent();
            this.trigger('on_before_add', new_row, container);
            row.after(new_row);
            this.init_row(container, new_row);
        }
        remove_handle(evt) {
            evt.preventDefault();
            const row = this.get_row(evt.currentTarget);
            this.trigger('on_remove', row);
            const container = row.parent();
            row.remove();
            this.reset_indices(container);
        }
        up_handle(evt) {
            evt.preventDefault();
            const row = this.get_row(evt.currentTarget);
            this.trigger('on_before_up', row);
            row.insertBefore(row.prev());
            this.reset_indices(row.parent());
            this.trigger('on_up', row);
        }
        down_handle(evt) {
            evt.preventDefault();
            const row = this.get_row(evt.currentTarget);
            this.trigger('on_before_down', row);
            row.insertAfter(row.next());
            this.reset_indices(row.parent());
            this.trigger('on_down', row);
        }
    }

    const hooks = {
        before_add: {},
        add: {},
        remove: {},
        before_up: {},
        up: {},
        before_down: {},
        down: {},
        index: {},
    };
    const _array_subscribers = {
        on_before_add: [],
        on_add: [],
        on_remove: [],
        on_before_up: [],
        on_up: [],
        on_before_down: [],
        on_down: [],
        on_index: [],
    };
    function on_array_event(event, subscriber) {
        _array_subscribers[event].push(subscriber);
    }
    function inside_template(elem) {
        return elem.parents('.arraytemplate').length > 0;
    }
    class ArrayWidget extends ArrayBase {
        static initialize(context) {
            $('div.array', context).each(function () {
                const wrapper = $(this);
                if (wrapper.attr('id').indexOf('-TEMPLATE') === -1) {
                    new ArrayWidget(wrapper);
                }
            });
        }
        constructor(wrapper) {
            super(wrapper);
            this.hooks = hooks;
            this._array_subscribers = _array_subscribers;
            this.array_widget = ArrayWidget;
            this.icon_add = 'icon-plus-sign';
            this.icon_remove = 'icon-minus-sign';
            this.icon_up = 'icon-circle-arrow-up';
            this.icon_down = 'icon-circle-arrow-down';
        }
    }

    $(() => {
        if (window.ts !== undefined) {
            ts.ajax.register(ArrayWidget.initialize, true);
        } else if (window.bdajax !== undefined) {
            bdajax.register(ArrayWidget.initialize, true);
        } else {
            ArrayWidget.initialize();
        }
    });

    exports.ArrayWidget = ArrayWidget;
    exports.hooks = hooks;
    exports.inside_template = inside_template;
    exports.on_array_event = on_array_event;

    Object.defineProperty(exports, '__esModule', { value: true });


    window.yafowil = window.yafowil || {};
    window.yafowil.array = exports;


    return exports;

})({}, jQuery);
