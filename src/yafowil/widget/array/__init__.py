import os
from yafowil.base import factory
try:
    # try to provide as fanstatic resource
    from js.jquery import jquery
    from fanstatic import (
        Library,
        Resource,
    )
    library = Library('yafowil.widget.array', 'resources')
    # XXX depends jquery - fanstatic seems to render resources multiple times?
    js = Resource(library, 'widget.js') # , depends=[jquery])
    #js = Resource(library, 'widget.js', depends=[jquery])
    default = Resource(library, 'default/widget.css')
    # XXX depends js.bootstrap
    bootstrap = Resource(library, 'bootstrap/widget.css')
    def register():
        import widget
        factory.register_theme('default', 'yafowil.widget.array',
                               js=[js], css=[default])
        factory.register_theme('bootstrap', 'yafowil.widget.array',
                               js=[js], css=[bootstrap])
except ImportError:
    # provide ourself if fanstatic not installed
    library = None
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