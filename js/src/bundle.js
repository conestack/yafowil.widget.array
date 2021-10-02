import $ from 'jquery';

import {ArrayWidget} from './widget.js';

export * from './widget.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(ArrayWidget.initialize, true);
    } else {
        ArrayWidget.initialize();
    }
});
