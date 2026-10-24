import $ from 'jquery';
import { ArrayBase } from '../src/base/array.js';
import { ArrayWidget, hooks, inside_template, on_array_event } from '../src/bootstrap5/widget.js';

const subscribed = [];
on_array_event('on_add', (inst, row) => {
    subscribed.push([inst, row]);
});

function input_widget(index) {
    const value = index === 'TEMPLATE' ? '' : index;
    return `<input id="input-myform-myarray-${index}" name="myform.myarray.${index}"
                   value="${value}" />`;
}

// Markup of yafowil.widget.dict as array entry. The table id contains the
// dotted path of the widget.
function dict_widget(index) {
    const key = index === 'TEMPLATE' ? '' : index;
    return `
        <fieldset>
          <table id="dictwidget_myform.myarray.${index}.entry">
            <tbody>
              <tr>
                <td class="key">
                  <input id="input-myform-myarray-${index}-entry0-key"
                         name="myform.myarray.${index}.entry.0.key" value="${key}" />
                </td>
              </tr>
            </tbody>
          </table>
        </fieldset>`;
}

function create_array(entries, widget = input_widget) {
    let body = '';
    for (let i = 0; i < entries; i++) {
        body += `
            <tr>
              <td class="widget">${widget(i)}</td>
              <td class="actions">
                <div class="array_actions">
                  <a class="array_row_add" href="#"></a>
                  <a class="array_row_remove" href="#"></a>
                  <a class="array_row_up" href="#"></a>
                  <a class="array_row_down" href="#"></a>
                </div>
              </td>
            </tr>`;
    }
    return $(`
        <div class="array array-add array-remove array-sort" id="array-myform-myarray">
          <table>
            <thead>
              <tr>
                <th class="head_actions">
                  <div class="array_actions"><a class="array_row_add" href="#"></a></div>
                </th>
              </tr>
            </thead>
            <tbody>${body}</tbody>
          </table>
          <div class="arraytemplate">${widget('TEMPLATE')}</div>
        </div>`).appendTo('body');
}

function rows(wrapper) {
    return $('> table > tbody > tr', wrapper);
}

function row_values(wrapper) {
    return rows(wrapper)
        .map((_, row) => $('input', row).val())
        .get();
}

QUnit.module('bootstrap5 ArrayWidget', (test_hooks) => {
    const orig_set_timeout = window.setTimeout;
    let wrapper, timeouts;

    test_hooks.beforeEach(() => {
        subscribed.length = 0;
        timeouts = [];
        // run highlight timeouts on demand instead of waiting
        window.setTimeout = (fn, delay) => {
            timeouts.push([fn, delay]);
        };
    });
    test_hooks.afterEach(() => {
        window.setTimeout = orig_set_timeout;
        if (wrapper) {
            wrapper.remove();
            wrapper = null;
        }
    });

    function run_timeouts(assert) {
        for (const [fn, delay] of timeouts) {
            assert.strictEqual(delay, 1000);
            fn();
        }
        timeouts = [];
    }

    QUnit.test('initialize', (assert) => {
        wrapper = create_array(0);
        const template = $('<div class="array" id="array-myform-sub-TEMPLATE" />').appendTo('body');
        ArrayWidget.initialize();
        const wid = wrapper.data('yafowil-array');
        assert.true(wid instanceof ArrayWidget);
        assert.true(wid instanceof ArrayBase);
        assert.strictEqual(template.data('yafowil-array'), undefined);
        template.remove();

        assert.strictEqual(wid.hooks, hooks);
        assert.strictEqual(wid.array_widget, ArrayWidget);
        assert.strictEqual(wid.icon_add, 'bi-plus-circle-fill');
        assert.strictEqual(wid.icon_remove, 'bi-dash-circle-fill');
        assert.strictEqual(wid.icon_up, 'bi-arrow-up-circle-fill');
        assert.strictEqual(wid.icon_down, 'bi-arrow-down-circle-fill');
    });

    QUnit.test('create_row highlights new row', (assert) => {
        wrapper = create_array(0);
        const wid = new ArrayWidget(wrapper);
        const row = wid.create_row();
        assert.deepEqual(
            $('td.actions span', row)
                .map((_, el) => el.className)
                .get(),
            [
                'bi-plus-circle-fill',
                'bi-dash-circle-fill',
                'bi-arrow-up-circle-fill',
                'bi-arrow-down-circle-fill',
            ],
        );
        assert.true(row.hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(row.hasClass('row-moved'));
    });

    QUnit.test('add row', (assert) => {
        wrapper = create_array(1);
        const wid = new ArrayWidget(wrapper);
        $('> table > thead a.array_row_add', wrapper).trigger('click');
        assert.deepEqual(row_values(wrapper), ['', '0']);
        const new_row = rows(wrapper).first();
        assert.true(new_row.hasClass('row-moved'));
        assert.strictEqual(subscribed.length, 1);
        assert.strictEqual(subscribed[0][0], wid);
        assert.true(subscribed[0][1].is(new_row));
        run_timeouts(assert);
        assert.false(new_row.hasClass('row-moved'));
    });

    QUnit.test('move row up highlights row', (assert) => {
        wrapper = create_array(2);
        new ArrayWidget(wrapper);
        const row = rows(wrapper).last();
        $('a.array_row_up', row).trigger('click');
        assert.deepEqual(row_values(wrapper), ['1', '0']);
        assert.strictEqual($('input', row).attr('name'), 'myform.myarray.0');
        assert.true(row.hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(row.hasClass('row-moved'));
    });

    QUnit.test('move row down highlights row', (assert) => {
        wrapper = create_array(2);
        new ArrayWidget(wrapper);
        const row = rows(wrapper).first();
        $('a.array_row_down', row).trigger('click');
        assert.deepEqual(row_values(wrapper), ['1', '0']);
        assert.strictEqual($('input', row).attr('name'), 'myform.myarray.1');
        assert.true(row.hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(row.hasClass('row-moved'));
    });

    QUnit.test('dict table id inside row survives add, remove and move', (assert) => {
        wrapper = create_array(2, dict_widget);
        new ArrayWidget(wrapper);

        function assert_rows(keys) {
            assert.deepEqual(
                $('td.key input', rows(wrapper))
                    .map((_, el) => el.value)
                    .get(),
                keys,
            );
            rows(wrapper).each(function (index) {
                const key = $('td.key input', this);
                assert.strictEqual(
                    $('table', this).attr('id'),
                    `dictwidget_myform.myarray.${index}.entry`,
                );
                assert.strictEqual(key.attr('id'), `input-myform-myarray-${index}-entry0-key`);
                assert.strictEqual(key.attr('name'), `myform.myarray.${index}.entry.0.key`);
            });
        }

        $('a.array_row_add', rows(wrapper).first()).trigger('click');
        assert_rows(['0', '', '1']);
        $('a.array_row_remove', rows(wrapper).first()).trigger('click');
        assert_rows(['', '1']);
        $('a.array_row_up', rows(wrapper).last()).trigger('click');
        assert_rows(['1', '']);
        $('a.array_row_down', rows(wrapper).first()).trigger('click');
        assert_rows(['', '1']);
        run_timeouts(assert);
    });

    QUnit.test('inside_template', (assert) => {
        wrapper = create_array(1);
        assert.true(inside_template($('> .arraytemplate input', wrapper)));
        assert.false(inside_template($('> table input', wrapper)));
    });
});
