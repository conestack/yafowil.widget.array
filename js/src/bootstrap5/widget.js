import $ from 'jquery';
import { ArrayBase } from '../array.js';

/**
 * Legacy hooks object for backward compatibility, providing deprecated event hooks.
 */
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

/**
 * Global subscribers for array events, called by each array instance.
 */
let _array_subscribers = {
    on_before_add: [],
    on_add: [],
    on_remove: [],
    on_before_up: [],
    on_up: [],
    on_before_down: [],
    on_down: [],
    on_index: []
};

/**
 * Registers a subscriber to a specified array event.
 */
export function on_array_event(event, subscriber) {
    _array_subscribers[event].push(subscriber);
}

/**
 * Checks if the specified element is within an array template.
 */
export function inside_template(elem) {
    return elem.parents('.arraytemplate').length > 0;
}

export class ArrayWidget extends ArrayBase {

    /**
     * @param {HTMLElement} context - DOM context for widget initialization.
     */
    static initialize(context) {
        $('div.array', context).each(function() {
            let wrapper = $(this);
            if (wrapper.attr('id').indexOf('-TEMPLATE') === -1) {
                new ArrayWidget(wrapper);
            }
        });
    }

    /**
     * @param {jQuery} wrapper - The jQuery-wrapped element to initialize.
     */
    constructor(wrapper) {
        super(wrapper);
        this.hooks = hooks;
        this._array_subscribers = _array_subscribers;
        this.array_widget = ArrayWidget;
        this.icon_add = 'bi-plus-circle-fill';
        this.icon_remove = 'bi-dash-circle-fill';
        this.icon_up = 'bi-arrow-up-circle-fill';
        this.icon_down = 'bi-arrow-down-circle-fill';
    }

    /**
     * Handles the event for moving a row up and applies a visual effect.
     * 
     * @param {Event} evt
     */
    up_handle(evt) {
        super.up_handle(evt);
        const row = this.get_row(evt.currentTarget);
        row.addClass('row-moved');
        setTimeout(() => {
            row.removeClass('row-moved');
        }, 1000);
    }

    /**
     * Handles the event for moving a row down and applies a visual effect.
     * 
     * @param {Event} evt
     */
    down_handle(evt) {
        super.down_handle(evt);
        const row = this.get_row(evt.currentTarget);
        row.addClass('row-moved');
        setTimeout(() => {
            row.removeClass('row-moved');
        }, 1000);
    }

    /**
     * Creates a new row with a visual effect.
     * 
     * @returns {jQuery} - The created row element.
     */
    create_row() {
        const row = super.create_row();
        row.addClass('row-moved');
        setTimeout(() => {
            row.removeClass('row-moved');
        }, 1000);
        return row;
    }
}
