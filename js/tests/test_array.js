import { ArrayWidget } from "../src/widget";

QUnit.test('Initialize', assert => {
    let el = $('<div class="array" id="test" />').appendTo('body');
    ArrayWidget.initialize();

    let wid = el.data('yafowil-array');
    assert.ok(wid);
    assert.true(wid instanceof ArrayWidget);

    el.remove();
    wid = null;
});
