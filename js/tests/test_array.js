import $ from 'jquery';
import { ArrayBase } from '../src/base/array.js';
import { ArrayWidget, hooks, inside_template, on_array_event } from '../src/default/widget.js';

const event_names = [
    'on_before_add',
    'on_add',
    'on_remove',
    'on_before_up',
    'on_up',
    'on_before_down',
    'on_down',
    'on_index',
];

// Array subscribers are global and cannot be unregistered, subscribe once and
// reset the recorded events before each test.
const events = [];
for (const name of event_names) {
    on_array_event(name, (...args) => {
        events.push([name, ...args]);
    });
}

function events_of(name) {
    return events.filter((e) => e[0] === name);
}

const all_actions =
    '<a class="array_row_add" href="#"><span class="icon-plus-sign"> </span></a>' +
    '<a class="array_row_remove" href="#"><span class="icon-minus-sign"> </span></a>' +
    '<a class="array_row_up" href="#"><span class="icon-circle-arrow-up"> </span></a>' +
    '<a class="array_row_down" href="#"><span class="icon-circle-arrow-down"> </span></a>';

function field_widget(index) {
    const value = index === 'TEMPLATE' ? '' : index;
    return `
        <div class="field" id="field-myform-myarray-${index}">
          <label for="input-myform-myarray-${index}">My Field</label>
          <input class="text" id="input-myform-myarray-${index}"
                 name="myform.myarray.${index}" type="text" value="${value}" />
        </div>`;
}

// Markup of yafowil.widget.dict as array entry. The table id contains the
// dotted path of the widget.
function dict_widget(index, path = 'myform.myarray') {
    const id_path = path.replace(/\./g, '-'),
        key = index === 'TEMPLATE' ? '' : index;
    return `
        <input id="input-${id_path}-${index}-exists" name="${path}.${index}.exists"
               type="hidden" value="1" />
        <fieldset>
          <table id="dictwidget_${path}.${index}.entry">
            <tbody>
              <tr>
                <td class="key">
                  <input id="input-${id_path}-${index}-entry0-key"
                         name="${path}.${index}.entry.0.key" value="${key}" />
                </td>
              </tr>
            </tbody>
          </table>
        </fieldset>`;
}

function create_entry(index, widget) {
    return `
        <tr>
          <td class="widget">${widget(index)}</td>
          <td class="actions">
            <div class="array_actions">${all_actions}</div>
          </td>
        </tr>`;
}

function create_array(opts = {}) {
    const css = opts.css ?? 'array-add array-remove array-sort',
        widget = opts.widget ?? field_widget;
    let entries = '';
    for (let i = 0; i < (opts.entries ?? 0); i++) {
        entries += create_entry(i, widget);
    }
    return $(`
        <div class="array ${css}" id="${opts.id ?? 'array-myform-myarray'}">
          <table>
            <thead>
              <tr>
                <th>My Array</th>
                <th class="head_actions">
                  <div class="array_actions">
                    <a class="array_row_add" href="#">
                      <span class="icon-plus-sign"> </span>
                    </a>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>${entries}</tbody>
          </table>
          <div class="arraytemplate">${opts.template ?? widget('TEMPLATE')}</div>
        </div>`).appendTo('body');
}

function rows(wrapper) {
    return $('> table > tbody > tr', wrapper);
}

function row_values(wrapper) {
    return rows(wrapper)
        .map(function () {
            return $('input', this).val();
        })
        .get();
}

function assert_indices(assert, wrapper) {
    rows(wrapper).each(function (index) {
        const field = $('div.field', this);
        assert.strictEqual(field.attr('id'), `field-myform-myarray-${index}`);
        assert.strictEqual($('label', field).attr('for'), `input-myform-myarray-${index}`);
        assert.strictEqual($('input', field).attr('id'), `input-myform-myarray-${index}`);
        assert.strictEqual($('input', field).attr('name'), `myform.myarray.${index}`);
    });
}

function assert_dict_rows(assert, wrapper, keys) {
    const key_inputs = $('td.key input', rows(wrapper));
    assert.deepEqual(key_inputs.map((_, el) => el.value).get(), keys);
    rows(wrapper).each(function (index) {
        const exists = $('input[type="hidden"]', this),
            key = $('td.key input', this);
        assert.strictEqual($('table', this).attr('id'), `dictwidget_myform.myarray.${index}.entry`);
        assert.strictEqual(exists.attr('id'), `input-myform-myarray-${index}-exists`);
        assert.strictEqual(exists.attr('name'), `myform.myarray.${index}.exists`);
        assert.strictEqual(key.attr('id'), `input-myform-myarray-${index}-entry0-key`);
        assert.strictEqual(key.attr('name'), `myform.myarray.${index}.entry.0.key`);
    });
}

function click(elem) {
    const evt = $.Event('click');
    elem.trigger(evt);
    return evt;
}

QUnit.module('ArrayWidget', (test_hooks) => {
    let wrapper;

    test_hooks.beforeEach(() => {
        events.length = 0;
    });
    test_hooks.afterEach(() => {
        if (wrapper) {
            wrapper.remove();
            wrapper = null;
        }
    });

    QUnit.test('Initialize', (assert) => {
        const el = $('<div class="array" id="test" />').appendTo('body');
        ArrayWidget.initialize();

        let wid = el.data('yafowil-array');
        assert.ok(wid);
        assert.true(wid instanceof ArrayWidget);

        el.remove();
        wid = null;
    });

    QUnit.test('initialize skips array templates', (assert) => {
        wrapper = $('<div class="array" id="array-myform-myarray-TEMPLATE" />').appendTo('body');
        ArrayWidget.initialize();
        assert.strictEqual(wrapper.data('yafowil-array'), undefined);
    });

    QUnit.test('initialize respects context', (assert) => {
        wrapper = create_array();
        ArrayWidget.initialize($('<div />'));
        assert.strictEqual(wrapper.data('yafowil-array'), undefined);
        ArrayWidget.initialize(wrapper.parent());
        assert.true(wrapper.data('yafowil-array') instanceof ArrayWidget);
    });

    QUnit.test('constructor', (assert) => {
        wrapper = create_array();
        const wid = new ArrayWidget(wrapper);
        assert.true(wid instanceof ArrayBase);
        assert.strictEqual(wrapper.data('yafowil-array'), wid);
        assert.true(wid.wrapper.is(wrapper));
        assert.true(wid.table.is($('> table', wrapper)));
        assert.strictEqual(wid.hooks, hooks);
        assert.strictEqual(wid.array_widget, ArrayWidget);
        assert.strictEqual(wid.icon_add, 'icon-plus-sign');
        assert.strictEqual(wid.icon_remove, 'icon-minus-sign');
        assert.strictEqual(wid.icon_up, 'icon-circle-arrow-up');
        assert.strictEqual(wid.icon_down, 'icon-circle-arrow-down');
        assert.strictEqual(wid.base_id, 'myform-myarray');
    });

    QUnit.test('mark disabled', (assert) => {
        wrapper = create_array({ entries: 3 });
        new ArrayWidget(wrapper);
        const up = $('a.array_row_up', wrapper);
        const down = $('a.array_row_down', wrapper);
        assert.deepEqual(up.map((_, el) => $(el).hasClass('array_row_up_disabled')).get(), [
            true,
            false,
            false,
        ]);
        assert.deepEqual(down.map((_, el) => $(el).hasClass('array_row_down_disabled')).get(), [
            false,
            false,
            true,
        ]);
    });

    QUnit.test('create_row', (assert) => {
        wrapper = create_array();
        const wid = new ArrayWidget(wrapper);
        const row = wid.create_row();
        assert.strictEqual(row.length, 1);
        assert.true(row.is('tr'));
        assert.strictEqual(
            $('td.widget div.field', row).attr('id'),
            'field-myform-myarray-TEMPLATE',
        );
        // template itself is cloned, not moved
        assert.strictEqual($('> .arraytemplate div.field', wrapper).length, 1);
        const actions = $('td.actions .array_actions a', row);
        assert.deepEqual(actions.map((_, el) => el.className).get(), [
            'array_row_add',
            'array_row_remove',
            'array_row_up',
            'array_row_down',
        ]);
        assert.deepEqual(
            $('span', actions)
                .map((_, el) => el.className)
                .get(),
            ['icon-plus-sign', 'icon-minus-sign', 'icon-circle-arrow-up', 'icon-circle-arrow-down'],
        );
    });

    QUnit.test('create_row without actions', (assert) => {
        wrapper = create_array({ css: '' });
        const wid = new ArrayWidget(wrapper);
        const row = wid.create_row();
        assert.strictEqual($('td.actions', row).length, 1);
        assert.strictEqual($('td.actions .array_actions a', row).length, 0);
    });

    QUnit.test('create_row static', (assert) => {
        wrapper = create_array({ css: 'array-static array-add array-remove array-sort' });
        const wid = new ArrayWidget(wrapper);
        const row = wid.create_row();
        assert.strictEqual($('td', row).length, 1);
        assert.strictEqual($('td.actions', row).length, 0);
    });

    QUnit.test('add first row', (assert) => {
        wrapper = create_array({ entries: 2 });
        const wid = new ArrayWidget(wrapper);
        const evt = click($('> table > thead a.array_row_add', wrapper));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_values(wrapper), ['', '0', '1']);
        assert_indices(assert, wrapper);

        const new_row = rows(wrapper).first();
        const container = $('> table > tbody', wrapper);
        const before_add = events_of('on_before_add');
        assert.strictEqual(before_add.length, 1);
        assert.strictEqual(before_add[0][1], wid);
        assert.true(before_add[0][2].is(new_row));
        assert.true(before_add[0][3].is(container));
        const on_add = events_of('on_add');
        assert.strictEqual(on_add.length, 1);
        assert.strictEqual(on_add[0][1], wid);
        assert.true(on_add[0][2].is(new_row));
        const on_index = events_of('on_index');
        assert.deepEqual(
            on_index.map((e) => e[3]),
            [0, 1, 2],
        );
        assert.true(on_index[0][2].is(new_row));

        // actions of new row are bound
        click($('a.array_row_remove', new_row));
        assert.deepEqual(row_values(wrapper), ['0', '1']);
    });

    QUnit.test('add row', (assert) => {
        wrapper = create_array({ entries: 2 });
        const wid = new ArrayWidget(wrapper);
        const evt = click($('a.array_row_add', rows(wrapper).first()));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_values(wrapper), ['0', '', '1']);
        assert_indices(assert, wrapper);

        const new_row = rows(wrapper).eq(1);
        const before_add = events_of('on_before_add');
        assert.strictEqual(before_add.length, 1);
        assert.strictEqual(before_add[0][1], wid);
        assert.true(before_add[0][2].is(new_row));
        assert.true(before_add[0][3].is($('> table > tbody', wrapper)));
        assert.true(events_of('on_add')[0][2].is(new_row));
        assert.true(
            $('a.array_row_down', rows(wrapper).last()).hasClass('array_row_down_disabled'),
        );
        assert.false($('a.array_row_down', new_row).hasClass('array_row_down_disabled'));
    });

    QUnit.test('remove row', (assert) => {
        wrapper = create_array({ entries: 3 });
        const wid = new ArrayWidget(wrapper);
        const row = rows(wrapper).eq(1);
        const evt = click($('a.array_row_remove', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_values(wrapper), ['0', '2']);
        assert_indices(assert, wrapper);

        const on_remove = events_of('on_remove');
        assert.strictEqual(on_remove.length, 1);
        assert.strictEqual(on_remove[0][1], wid);
        assert.true(on_remove[0][2].is(row));
        assert.strictEqual(events_of('on_index').length, 2);
    });

    QUnit.test('move row up', (assert) => {
        wrapper = create_array({ entries: 3 });
        const wid = new ArrayWidget(wrapper);
        const row = rows(wrapper).eq(2);
        const evt = click($('a.array_row_up', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_values(wrapper), ['0', '2', '1']);
        assert_indices(assert, wrapper);
        assert.deepEqual(
            events.filter((e) => e[0] !== 'on_index').map((e) => e[0]),
            ['on_before_up', 'on_up'],
        );
        assert.strictEqual(events_of('on_up')[0][1], wid);
        assert.true(events_of('on_before_up')[0][2].is(row));
        assert.true(events_of('on_up')[0][2].is(row));
        assert.false($('a.array_row_down', row).hasClass('array_row_down_disabled'));
        assert.true(
            $('a.array_row_down', rows(wrapper).last()).hasClass('array_row_down_disabled'),
        );
    });

    QUnit.test('move row down', (assert) => {
        wrapper = create_array({ entries: 3 });
        const wid = new ArrayWidget(wrapper);
        const row = rows(wrapper).eq(0);
        const evt = click($('a.array_row_down', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_values(wrapper), ['1', '0', '2']);
        assert_indices(assert, wrapper);
        assert.deepEqual(
            events.filter((e) => e[0] !== 'on_index').map((e) => e[0]),
            ['on_before_down', 'on_down'],
        );
        assert.strictEqual(events_of('on_down')[0][1], wid);
        assert.true(events_of('on_before_down')[0][2].is(row));
        assert.true(events_of('on_down')[0][2].is(row));
        assert.false($('a.array_row_up', row).hasClass('array_row_up_disabled'));
        assert.true($('a.array_row_up', rows(wrapper).first()).hasClass('array_row_up_disabled'));
    });

    QUnit.test('set_value_index', (assert) => {
        wrapper = create_array();
        const wid = new ArrayWidget(wrapper);
        assert.strictEqual(
            wid.set_value_index('input-myform-myarray-TEMPLATE', 'myform-myarray', 3, '-'),
            'input-myform-myarray-3',
        );
        assert.strictEqual(
            wid.set_value_index('input-myform-myarray-TEMPLATE-sub', 'myform-myarray', 3, '-'),
            'input-myform-myarray-3-sub',
        );
        assert.strictEqual(
            wid.set_value_index('myform.myarray.1.sub', 'myform.myarray', 0, '.'),
            'myform.myarray.0.sub',
        );
    });

    QUnit.test('set_value_index keeps the rest of the value', (assert) => {
        wrapper = create_array();
        const wid = new ArrayWidget(wrapper);
        assert.strictEqual(
            wid.set_value_index('dictwidget_arr.0.entry', 'arr', 3, '.'),
            'dictwidget_arr.3.entry',
        );
        assert.strictEqual(
            wid.set_value_index('myform.myarray.TEMPLATE-exists', 'myform.myarray', 3, '.'),
            'myform.myarray.3-exists',
        );
        assert.strictEqual(
            wid.set_value_index('myform.myarray.TEMPLATE.lat', 'myform.myarray', 3, '.'),
            'myform.myarray.3.lat',
        );
        assert.strictEqual(
            wid.set_value_index('input-myform-myarray-1-entry0-key', 'myform-myarray', 3, '-'),
            'input-myform-myarray-3-entry0-key',
        );
    });

    QUnit.test('set_value_index matches base at delimiters only', (assert) => {
        wrapper = create_array();
        const wid = new ArrayWidget(wrapper);
        // base inside the id prefix
        assert.strictEqual(
            wid.set_value_index('array-arr-TEMPLATE-sub', 'arr', 3, '-'),
            'array-arr-3-sub',
        );
        // base equals the id prefix
        assert.strictEqual(wid.set_value_index('input-input-0', 'input', 3, '-'), 'input-input-3');
        // base at the end of another name
        assert.strictEqual(wid.set_value_index('input-myarr-0', 'arr', 3, '-'), 'input-myarr-0');
        // base at the start of another name
        assert.strictEqual(
            wid.set_value_index('dictwidget_arr2.0.entry', 'arr', 3, '.'),
            'dictwidget_arr2.0.entry',
        );
        // base followed by a name which is not an index
        assert.strictEqual(
            wid.set_value_index('input-arr-sub-0', 'arr', 3, '-'),
            'input-arr-sub-0',
        );
        assert.strictEqual(wid.set_value_index('input-arr', 'arr', 3, '-'), 'input-arr');
    });

    QUnit.test('dict table id inside row survives add, remove and move', (assert) => {
        wrapper = create_array({ entries: 3, widget: dict_widget });
        new ArrayWidget(wrapper);
        click($('> table > thead a.array_row_add', wrapper));
        assert_dict_rows(assert, wrapper, ['', '0', '1', '2']);
        click($('a.array_row_add', rows(wrapper).eq(1)));
        assert_dict_rows(assert, wrapper, ['', '0', '', '1', '2']);
        click($('a.array_row_remove', rows(wrapper).eq(0)));
        assert_dict_rows(assert, wrapper, ['0', '', '1', '2']);
        click($('a.array_row_up', rows(wrapper).eq(3)));
        assert_dict_rows(assert, wrapper, ['0', '', '2', '1']);
        click($('a.array_row_down', rows(wrapper).eq(0)));
        assert_dict_rows(assert, wrapper, ['', '0', '2', '1']);
    });

    QUnit.test('dict table id inside row of root array keeps its suffix', (assert) => {
        wrapper = create_array({
            id: 'array-arr',
            entries: 2,
            widget: (index) => dict_widget(index, 'arr'),
        });
        new ArrayWidget(wrapper);
        click($('a.array_row_down', rows(wrapper).eq(0)));
        assert.deepEqual(
            $('table', rows(wrapper))
                .map((_, el) => el.id)
                .get(),
            ['dictwidget_arr.0.entry', 'dictwidget_arr.1.entry'],
        );
        assert.deepEqual(
            $('td.key input', rows(wrapper))
                .map((_, el) => el.value)
                .get(),
            ['1', '0'],
        );
    });

    QUnit.test('nested array id inside row of root array', (assert) => {
        // the root array name is part of the ``array-`` id prefix
        wrapper = create_array({
            id: 'array-arr',
            template: `
                <div class="array array-add" id="array-arr-TEMPLATE-sub">
                  <table><thead></thead><tbody></tbody></table>
                </div>`,
        });
        new ArrayWidget(wrapper);
        click($('> table > thead a.array_row_add', wrapper));
        assert.strictEqual($('div.array', rows(wrapper)).attr('id'), 'array-arr-0-sub');
    });

    QUnit.test('name suffix after index is kept', (assert) => {
        // markup of a checkbox as array entry
        wrapper = create_array({
            entries: 1,
            widget: (index) => `
                <input id="input-myform-myarray-${index}" name="myform.myarray.${index}"
                       type="checkbox" />
                <input id="checkboxexists-myform-myarray-${index}"
                       name="myform.myarray.${index}-exists" type="hidden"
                       value="checkboxexists" />`,
        });
        new ArrayWidget(wrapper);
        click($('> table > thead a.array_row_add', wrapper));
        const names = $('input', rows(wrapper))
            .map((_, el) => el.name)
            .get();
        assert.deepEqual(names, [
            'myform.myarray.0',
            'myform.myarray.0-exists',
            'myform.myarray.1',
            'myform.myarray.1-exists',
        ]);
        assert.strictEqual(
            $('input[type="hidden"]', rows(wrapper).last()).attr('id'),
            'checkboxexists-myform-myarray-1',
        );
    });

    QUnit.test('set_attr_index', (assert) => {
        wrapper = create_array();
        const wid = new ArrayWidget(wrapper);
        const node = $('<input id="input-other-TEMPLATE" name="myform.myarray.TEMPLATE" />');
        wid.set_attr_index(node, 'id', 'myform-myarray', 1, '-');
        wid.set_attr_index(node, 'for', 'myform-myarray', 1, '-');
        wid.set_attr_index(node, 'name', 'myform.myarray', 1, '.');
        assert.strictEqual(node.attr('id'), 'input-other-TEMPLATE');
        assert.strictEqual(node.attr('for'), undefined);
        assert.strictEqual(node.attr('name'), 'myform.myarray.1');
    });

    QUnit.test('nested array gets initialized on add', (assert) => {
        wrapper = create_array({
            template: `
                <div class="array array-add" id="array-myform-myarray-TEMPLATE-sub">
                  <table><thead></thead><tbody></tbody></table>
                </div>`,
        });
        const wid = new ArrayWidget(wrapper);
        click($('> table > thead a.array_row_add', wrapper));
        const nested = $('div.array', rows(wrapper).first());
        assert.strictEqual(nested.attr('id'), 'array-myform-myarray-0-sub');
        const nested_wid = nested.data('yafowil-array');
        assert.true(nested_wid instanceof ArrayWidget);
        assert.notStrictEqual(nested_wid, wid);
        // template of nested array is not initialized
        const nested_template = $('> .arraytemplate div.array', wrapper);
        assert.strictEqual(nested_template.data('yafowil-array'), undefined);
    });

    QUnit.test('deprecated hooks', (assert) => {
        const orig_log = console.log;
        const logged = [];
        console.log = (msg) => {
            logged.push(msg);
        };
        const hook_calls = [];
        hooks.add.my_hook = (...args) => {
            hook_calls.push(args);
        };
        try {
            wrapper = create_array();
            new ArrayWidget(wrapper);
            click($('> table > thead a.array_row_add', wrapper));
        } finally {
            console.log = orig_log;
            delete hooks.add.my_hook;
        }
        assert.deepEqual(logged, [
            'Array hooks are deprecated. Use ``on_array_event`` instead.',
            '    - my_hook',
        ]);
        assert.strictEqual(hook_calls.length, 1);
        assert.strictEqual(hook_calls[0].length, 1);
        assert.true(hook_calls[0][0].is(rows(wrapper).first()));
        // subscribers additionally get the array instance
        assert.strictEqual(events_of('on_add')[0][1], wrapper.data('yafowil-array'));
    });

    QUnit.test('inside_template', (assert) => {
        wrapper = create_array({ entries: 1 });
        assert.true(inside_template($('> .arraytemplate input', wrapper)));
        assert.false(inside_template($('> table input', wrapper)));
    });
});
