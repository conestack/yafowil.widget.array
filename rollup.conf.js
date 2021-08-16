import cleanup from 'rollup-plugin-cleanup';
import {terser} from 'rollup-plugin-terser';

const outro = `
if (window.yafowil === undefined) {
    window.yafowil = {};
}

window.yafowil.array = exports;
`;

export default args => {
    let conf = {
        input: 'js/src/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            file: 'src/yafowil/widget/array/yafowil.widget.array.js',
            format: 'iife',
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default',
            sourcemap: true,
            sourcemapExcludeSources: true
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        conf.output.push({
            file: 'src/yafowil/widget/array/yafowil.widget.array.min.js',
            format: 'iife',
            plugins: [
                terser()
            ],
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default',
            sourcemap: true,
            sourcemapExcludeSources: true
        });
    }
    return conf;
};
