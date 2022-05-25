from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Common
##############################################################################

# webresource ################################################################

scripts = wr.ResourceGroup(
    name='yafowil-array-scripts',
    path='yafowil.widget.array'
)
scripts.add(wr.ScriptResource(
    name='yafowil-array-js',
    depends='jquery-js',
    directory=resources_dir,
    resource='widget.js',
    compressed='widget.min.js'
))

# B/C resources ##############################################################

js = [{
    'group': 'yafowil.widget.array.common',
    'resource': 'widget.js',
    'order': 20,
}]


##############################################################################
# Default
##############################################################################

# webresource ################################################################

default_styles = wr.ResourceGroup(
    name='yafowil-array-styles',
    path='yafowil.widget.array'
)
default_styles.add(wr.StyleResource(
    name='yafowil-array-css',
    directory=os.path.join(resources_dir, 'default'),
    resource='widget.css'
))

# B/C resources ##############################################################

default_css = [{
    'group': 'yafowil.widget.array.common',
    'resource': 'default/widget.css',
    'order': 20,
}]


##############################################################################
# Bootstrap
##############################################################################

# webresource ################################################################

bootstrap_styles = wr.ResourceGroup(
    name='yafowil-array-styles',
    path='yafowil.widget.array'
)
bootstrap_styles.add(wr.StyleResource(
    name='yafowil-array-css',
    directory=os.path.join(resources_dir, 'bootstrap'),
    resource='widget.css'
))

# B/C resources ##############################################################

bootstrap_css = [{
    'group': 'yafowil.widget.array.common',
    'resource': 'bootstrap/widget.css',
    'order': 20,
}]


##############################################################################
# Plone5
##############################################################################

# webresource ################################################################

plone5_styles = wr.ResourceGroup(
    name='yafowil-array-styles',
    path='yafowil.widget.array'
)
plone5_styles.add(wr.StyleResource(
    name='yafowil-array-css',
    directory=os.path.join(resources_dir, 'plone5'),
    resource='widget.css'
))

# B/C resources ##############################################################

plone5_css = [{
    'group': 'yafowil.widget.array.common',
    'resource': 'plone5/widget.css',
    'order': 20,
}]


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    from yafowil.widget.array import widget  # noqa

    # Default
    factory.register_theme(
        'default', 'yafowil.widget.array', resources_dir,
        js=js, css=default_css
    )
    factory.register_scripts('default', 'yafowil.widget.array', scripts)
    factory.register_styles('default', 'yafowil.widget.array', default_styles)

    # Bootstrap
    factory.register_theme(
        ['bootstrap', 'bootstrap3'], 'yafowil.widget.array', resources_dir,
        js=js, css=bootstrap_css
    )
    factory.register_scripts(
        ['bootstrap', 'bootstrap3'],
        'yafowil.widget.array',
        scripts
    )
    factory.register_styles(
        ['bootstrap', 'bootstrap3'],
        'yafowil.widget.array',
        bootstrap_styles
    )

    # Plone 5
    factory.register_theme(
        'plone5', 'yafowil.widget.array', resources_dir,
        js=js, css=plone5_css
    )
    factory.register_scripts('plone5', 'yafowil.widget.array', scripts)
    factory.register_styles('plone5', 'yafowil.widget.array', plone5_styles)
