import os
from yafowil.base import factory


# XXX: use fanstatic
resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'group': 'yafowil.widget.array',
    'resource': 'widget.js',
    'order': 20,
}]

default_css = [{
    'group': 'yafowil.widget.array',
    'resource': 'default/widget.css',
    'order': 20,
}]

bootstrap_css = [{
    'group': 'yafowil.widget.array',
    'resource': 'bootstrap/widget.css',
    'order': 20,
}]


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.array',
                           resourcedir, js=js, css=default_css)
    factory.register_theme('bootstrap', 'yafowil.widget.array',
                           resourcedir, js=js, css=bootstrap_css)