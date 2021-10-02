import $ from 'jquery';

export let hooks = {
    before_add: {},
    add: {},
    remove: {},
    before_up: {},
    up: {},
    before_down: {},
    down: {},
    index: {}
};

export class ArrayWidget {

    static initialize(context) {
        $('div.array', context).each(function() {
            new ArrayWidget($(this));
        });
    }

    constructor(wrapper) {
        this.wrapper = wrapper;
        wrapper.data('array', this);
        let table = $('> table', wrapper),
            head_actions = $('> thead .array_actions', table),
            add_handle = this.add_first_handle.bind(this);
        this.table = table;
        $('a.array_row_add', head_actions).off().on('click', add_handle);
        this.bind_actions();
    }

    bind_actions() {
        let actions_sel = '> tbody > tr > td.actions .array_actions',
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
        let css = this.wrapper.attr('class');
        let row = '';
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
        let template = $('> .arraytemplate', this.wrapper).clone();
        $('.widget', row).append(template.children());
        return row;
    }

    get_row(action) {
        return $(action).parent().parent().parent();
    }

    get base_id() {
        let id = this.wrapper.attr('id');
        return id.substring(6, id.length);
    }

    reset_indices(context) {
        let index = 0,
            base_id = this.base_id,
            that = this,
            row;
        context.children().each(function() {
            row = $(this);
            that.set_row_index(row, base_id, index);
            that.notify_hooks(hooks.index, row, index);
            index++;
        });
        this.bind_actions();
    }

    set_row_index(node, base_id, index) {
        let base_name = base_id.replace(/\-/g, '.'),
            set_index = this.set_attr_index,
            child;
        node.children().each(function() {
            child = $(this);
            set_index(child, 'id', base_id, index, '-');
            set_index(child, 'for', base_id, index, '-');
            set_index(child, 'name', base_name, index, '.');
            if (child.attr('class').indexOf('array') > -1) {
                child.data('array').set_row_index(child, base_id, index);
            }
        });
    }

    set_attr_index(node, attr, base, index, delim) {
        let value = node.attr(attr);
        if (value && value.indexOf(base) > -1) {
            let idx_0 = value.indexOf(base) + base.length + 1,
                idx_1 = value.indexOf(delim, idx_0),
                pre = value.substring(0, idx_0),
                post = '';
            if (idx_1 > -1) {
                post = value.substring(idx_1, value.length);
            }
            node.attr(attr, pre + index + post);
        }
    }

    notify_hooks(hooks, ...args) {
        for (let name in hooks) {
            hooks[name].apply(null, args);
        }
    }

    add_first_handle(evt) {
        evt.preventDefault();
        let new_row = this.create_row(),
            container = $('> tbody', this.table);
        this.notify_hooks(hooks.before_add, new_row, container);
        container.prepend(new_row);
        ArrayWidget.initialize(new_row);
        this.reset_indices(container);
        this.notify_hooks(hooks.add, new_row);
    }

    add_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget),
            new_row = this.create_row(),
            container = row.parent();
        this.notify_hooks(hooks.before_add, new_row, container);
        row.after(new_row);
        this.reset_indices(container);
        this.notify_hooks(hooks.add, new_row);
    }

    remove_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        this.notify_hooks(hooks.remove, row);
        let container = row.parent();
        row.remove();
        this.reset_indices(container);
    }

    up_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        this.notify_hooks(hooks.before_up, row);
        row.insertBefore(row.prev());
        this.reset_indices(row.parent());
        this.notify_hooks(hooks.up, row);
    }

    down_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        this.notify_hooks(hooks.before_down, row);
        row.insertAfter(row.next());
        this.reset_indices(row.parent());
        this.notify_hooks(hooks.down, row);
    }
}
