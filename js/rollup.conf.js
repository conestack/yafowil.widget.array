import cleanup from 'rollup-plugin-cleanup';
import postcss from 'rollup-plugin-postcss';
import terser from '@rollup/plugin-terser';

const out_dir = 'src/yafowil/widget/array/resources';

const outro = `
window.yafowil = window.yafowil || {};
window.yafowil.array = exports;
`;

export default args => {

    ////////////////////////////////////////////////////////////////////////////
    // DEFAULT
    ////////////////////////////////////////////////////////////////////////////

    let bundle_default = {
        input: 'js/src/default/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_array',
            file: `${out_dir}/default/widget.js`,
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
        bundle_default.output.push({
            name: 'yafowil_array',
            file: `${out_dir}/default/widget.min.js`,
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
    let scss_default = {
        input: ['scss/default/widget.scss'],
        output: [
          {
            file: `${out_dir}/default/widget.css`,
            format: 'es',
            plugins: [terser()],
          },
        ],
        plugins: [
          postcss({
            extract: true,
            minimize: true,
            use: [
              ['sass', { outputStyle: 'compressed' }],
            ],
          }),
        ],
    };

    ////////////////////////////////////////////////////////////////////////////
    // BOOTSTRAP
    ////////////////////////////////////////////////////////////////////////////

    let scss_bootstrap = {
        input: ['scss/bootstrap/widget.scss'],
        output: [
          {
            file: `${out_dir}/bootstrap/widget.css`,
            format: 'es',
            plugins: [terser()],
          },
        ],
        plugins: [
          postcss({
            extract: true,
            minimize: true,
            use: [
              ['sass', { outputStyle: 'compressed' }],
            ],
          }),
        ],
    };

    ////////////////////////////////////////////////////////////////////////////
    // PLONE5
    ////////////////////////////////////////////////////////////////////////////

    let scss_plone5 = {
        input: ['scss/plone5/widget.scss'],
        output: [
          {
            file: `${out_dir}/plone5/widget.css`,
            format: 'es',
            plugins: [terser()],
          },
        ],
        plugins: [
          postcss({
            extract: true,
            minimize: true,
            use: [
              ['sass', { outputStyle: 'compressed' }],
            ],
          }),
        ],
    };

    ////////////////////////////////////////////////////////////////////////////
    // BOOTSTRAP5
    ////////////////////////////////////////////////////////////////////////////

    let bundle_bs5 = {
        input: 'js/src/bootstrap5/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_array',
            file: `${out_dir}/bootstrap5/widget.js`,
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
        bundle_bs5.output.push({
            name: 'yafowil_array',
            file: `${out_dir}/bootstrap5/widget.min.js`,
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
    let scss_bs5 = {
        input: ['scss/bootstrap5/widget.scss'],
        output: [{
            file: `${out_dir}/bootstrap5/widget.css`,
            format: 'es',
            plugins: [terser()],
        }],
        plugins: [
            postcss({
                extract: true,
                minimize: true,
                use: [
                    ['sass', { outputStyle: 'compressed' }],
                ],
            }),
        ],
    };

    return [bundle_default, scss_default, scss_bootstrap, scss_plone5, bundle_bs5, scss_bs5];
};
