import cleanup from 'rollup-plugin-cleanup';
import {terser} from 'rollup-plugin-terser';

const out_dir = 'src/yafowil/widget/array/resources/default';
const out_dir_bs5 = 'src/yafowil/widget/array/resources/bootstrap5';

const outro = `
window.yafowil = window.yafowil || {};
window.yafowil.array = exports;
`;

export default args => {
    // default
    let conf1 = {
        input: 'js/src/default/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_array',
            file: `${out_dir}/widget.js`,
            format: 'iife',
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        conf1.output.push({
            name: 'yafowil_array',
            file: `${out_dir}/widget.min.js`,
            format: 'iife',
            plugins: [
                terser()
            ],
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        });
    }

    // Bootstrap5
    let conf2 = {
        input: 'js/src/bootstrap5/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_array',
            file: `${out_dir_bs5}/widget.js`,
            format: 'iife',
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        conf2.output.push({
            name: 'yafowil_array',
            file: `${out_dir_bs5}/widget.min.js`,
            format: 'iife',
            plugins: [
                terser()
            ],
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        });
    }

    return [conf1, conf2];
};
