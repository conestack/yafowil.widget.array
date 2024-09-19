import $ from 'jquery';

import {ArrayWidget} from './widget_bs5.js';

export * from './widget_bs5.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(ArrayWidget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(ArrayWidget.initialize, true);
    } else {
        ArrayWidget.initialize();
    }
});
