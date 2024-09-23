import $ from 'jquery';
import {ArrayBase} from '../array.js';

// B/C. Deprecated. Use ``on_array_event``
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

// global array subscribers, gets called from every array instance
let _array_subscribers = {
    on_before_add: [],
    on_add: [],
    on_remove: [],
    on_before_up: [],
    on_up: [],
    on_before_down: [],
    on_down: [],
    on_index: []
}

export function on_array_event(event, subscriber) {
    _array_subscribers[event].push(subscriber)
}

export function inside_template(elem) {
    return elem.parents('.arraytemplate').length > 0
}

export class ArrayWidget extends ArrayBase {

    static initialize(context) {
        $('div.array', context).each(function() {
            let wrapper = $(this);
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
