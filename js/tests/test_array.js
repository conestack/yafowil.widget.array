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

function create_entry(index) {
    return `
        <tr>
          <td class="widget">
            <div class="field" id="field-myform-myarray-${index}">
              <label for="input-myform-myarray-${index}">My Field</label>
              <input class="text" id="input-myform-myarray-${index}"
                     name="myform.myarray.${index}" type="text" value="${index}" />
            </div>
          </td>
          <td class="actions">
            <div class="array_actions">${all_actions}</div>
          </td>
        </tr>`;
}

const template = `
    <div class="field" id="field-myform-myarray-TEMPLATE">
      <label for="input-myform-myarray-TEMPLATE">My Field</label>
      <input class="text" id="input-myform-myarray-TEMPLATE"
             name="myform.myarray.TEMPLATE" type="text" value="" />
    </div>`;

function create_array(opts = {}) {
    const css = opts.css ?? 'array-add array-remove array-sort';
    let entries = '';
    for (let i = 0; i < (opts.entries ?? 0); i++) {
        entries += create_entry(i);
    }
    return $(`
        <div class="array ${css}" id="array-myform-myarray">
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
          <div class="arraytemplate">${opts.template ?? template}</div>
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
