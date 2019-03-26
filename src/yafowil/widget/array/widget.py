from node.utils import UNSET
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.compat import ITER_TYPES
from yafowil.compound import compound_renderer
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops


@managedprops(*css_managed_props)
def array_display_proxy_renderer(widget, data):
    """B/C. Use ``display_proxy`` widget attribute.
    """
    input_attrs = {
        'type': 'hidden',
        'value': fetch_value(widget, data),
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),
        'required': attr_value('required', widget, data) and 'required' or None
    }
    return data.tag('input', **input_attrs) + data.rendered


factory.register(
    'array_display_proxy',
    extractors=[generic_extractor],
    edit_renderers=[array_display_proxy_renderer],
    display_renderers=[array_display_proxy_renderer])

# do not document internal widget
factory.doc['blueprint']['array_display_proxy'] = UNSET


ICON_CSS = {
    'add': 'icon-plus-sign',
    'remove': 'icon-minus-sign',
    'up': 'icon-circle-arrow-up',
    'down': 'icon-circle-arrow-down',
}


def actions_renderer(widget, data):
    tag = data.tag
    actions = list()
    for key in ['add', 'remove', 'up', 'down']:
        if widget.attrs.get(key):
            class_ = 'array_row_%s' % key
            icon = tag('span', ' ', class_=ICON_CSS[key])
            action = tag('a', icon, href='#', class_=class_)
            actions.append(action)
    kw = dict(class_='array_actions')
    return tag('div', *actions, **kw)


factory.register(
    'array_actions',
    edit_renderers=[actions_renderer])

# do not document internal widget
factory.doc['blueprint']['array_actions'] = UNSET


def array_builder(widget, factory):
    table = widget['table'] = factory('table', props={
        'structural': True,
        'class': widget.attrs['table_class'],
    })
    head = table['head'] = factory('thead', props={
        'structural': True,
    })
    row = head['row'] = factory('tr', props={
        'structural': True,
    })
    label = widget.attrs.get('label', u' ')
    if callable(label):
        label = label()
    row['label'] = factory('th', props={
        'structural': True,
        'label': label,
    })
    if not widget.attrs['static']:
        props = dict()
        props['structural'] = True
        props['th.class'] = 'head_actions'
        if widget.attrs['add']:
            props['add'] = True
        row['actions'] = factory('th:array_actions', props=props)
    table['body'] = factory('tbody', props={
        'structural': True,
    })


@managedprops('add', 'remove', 'sort', 'static', 'table_class', *css_managed_props)
def array_wrapper_renderer(widget, data):
    add_css = ''
    if not widget.attrs['static']:
        for attr in ['add', 'remove', 'sort']:
            if widget.attrs[attr]:
                add_css += ' array-%s' % attr
    else:
        add_css += ' array-static'
    kw = {
        'id': cssid(widget, 'array'),
        'class': cssclasses(widget, data) + add_css,
    }
    if 'array' not in kw['class'].split(' '):
        kw['class'] = 'array %s' % kw['class']
    rendered = data.rendered
    return data.tag('div', rendered, **kw)


CONTAINER = 'TEMPLATE_CONTAINER'
TEMPLATE = 'TEMPLATE'


def array_edit_renderer(widget, data):
    if len(widget) == 1 and CONTAINER not in widget:
        raise Exception(u"Empty array widget defined")
    if CONTAINER not in widget:
        template = widget.detach(widget.keys()[1])
        hook_array_template(widget, template)
    value = fetch_value(widget, data)
    # XXX: reset table body if already filled -> case form in memory.
    if value:
        widget.getter = UNSET
        data.value = UNSET
        template = widget[CONTAINER][TEMPLATE]
        create_array_children(widget, template, value)
    if not widget.attrs['add'] or widget.attrs['static']:
        del widget[CONTAINER]


def create_array_children(widget, template, value):
    if isinstance(value, dict):
        try:
            indices = [int(_) for _ in value.keys()]
        except ValueError as e:
            raise Exception(u"Array value error. %s" % str(e))
        indices = sorted(indices)
        for i in indices:
            create_array_entry(str(i), widget, template, value[str(i)])
    elif type(value) in ITER_TYPES:
        indices = range(len(value))
        for i in indices:
            create_array_entry(str(i), widget, template, value[i])
    else:
        raise ValueError(u"Expected list or dict as value. Got '{}'".format(
            str(type(value)))
        )


def create_array_entry(idx, widget, template, value):
    tbody = widget['table']['body']
    row = tbody['row_%s' % idx] = factory('tr', props={'structural': True})
    props = dict()
    props['structural'] = True
    props['class'] = 'widget'
    widget_col = row['widget_col'] = factory('td', props=props)
    if not widget.attrs['static']:
        props = dict()
        props['structural'] = True
        props['class'] = 'actions'
        actions_col = row['actions_col'] = factory('td', props=props)
        props = dict()
        props['structural'] = True
        if widget.attrs['add']:
            props['add'] = True
        if widget.attrs['remove']:
            props['remove'] = True
        if widget.attrs['sort']:
            props['up'] = True
            props['down'] = True
        actions_col['actions'] = factory('array_actions', props=props)
    child_widget = widget_col[idx] = duplicate_widget(template, value)
    if 'array' in template.blueprints:
        if len(template):
            create_array_entry_children(child_widget, template)
        orgin = template[template.keys()[-1]]
        template = duplicate_recursiv(orgin)
        hook_array_template(child_widget, template)
        # If array in array with compound. Compound template children get
        # hooked to array widget. Remove them.
        for key in child_widget.keys():
            if key not in ['table', CONTAINER]:
                del child_widget[key]
        return
    create_array_entry_children(child_widget, template)


def create_array_entry_children(widget, template):
    for name, child_template in template.items():
        child_widget = widget[name] = duplicate_recursiv(child_template)
        create_array_entry_children(child_widget, child_template)


def hook_array_template(widget, template):
    props = dict()
    props['structural'] = True
    props['class'] = 'arraytemplate'
    container = widget[CONTAINER] = factory('div', props=props)
    if template.attrs.get('structural'):
        raise Exception(
            u"Compound templates for arrays must not be structural.")
    container[TEMPLATE] = template


def duplicate_widget(widget, value=UNSET):
    blueprints = widget.blueprints
    leaf = len(widget) == 0
    # B/C: use display_property widget attribute!
    if leaf and (widget.mode == 'display' or widget.attrs.get('disabled')) \
            and 'array_display_proxy' not in blueprints:
        if not widget.attrs.get('display_proxy'):
            blueprints.insert(0, 'array_display_proxy')
    return factory(
        blueprints,
        value=value,
        props=widget.properties,
        custom=widget.custom,
        mode=widget.mode)


def duplicate_recursiv(widget):
    node = duplicate_widget(widget)
    for k, v in widget.items():
        node[k] = duplicate_recursiv(v)
    return node


def array_extractor(widget, data):
    template = widget[widget.keys()[-1]]
    helper = duplicate_recursiv(template)
    request = data.request
    ret = list()
    index = 0
    while True:
        helper.__parent__ = widget
        helper.__name__ = str(index)
        if not check_base_name_in_request(helper, request):
            break
        entry_data = helper.extract(request, parent=data)
        ret.append(entry_data.extracted)
        data[str(index)] = entry_data
        index += 1
    return ret


def check_base_name_in_request(widget, request):
    basename = widget.dottedpath
    for key in request.keys():
        if key.startswith(basename):
            return True
    return False


def set_display_mode(widget):
    for child in widget.values():
        child.mode = 'display'
        set_display_mode(child)


def array_display_renderer(widget, data):
    array_edit_renderer(widget, data)
    del widget['table']['head']['row']['actions']
    for row in widget['table']['body'].values():
        del row['actions_col']
    del widget[CONTAINER]
    set_display_mode(widget)


factory.register(
    'array',
    extractors=[array_extractor, generic_required_extractor],
    edit_renderers=[
        array_edit_renderer, compound_renderer, array_wrapper_renderer],
    display_renderers=[array_display_renderer, compound_renderer],
    builders=[array_builder])

factory.doc['blueprint']['array'] = \
"""Add-on widget `yafowil.widget.array
<http://github.com/bluedynamics/yafowil.widget.array/>`_.
"""

factory.defaults['array.class'] = 'array'

factory.defaults['array.required'] = False

factory.defaults['array.error_class'] = 'error'

factory.defaults['array.message_class'] = 'errormessage'

factory.defaults['array.table_class'] = None
factory.doc['props']['array.table_class'] = \
"""CSS classes rendered on array table.
"""

factory.defaults['array.static'] = False
factory.doc['props']['array.static'] = \
"""Array is immutable. No Array actions are rendered. If True, ``add``,
``remove`` and ``sort`` properties are ignored.
"""

factory.defaults['array.add'] = True
factory.doc['props']['array.add'] = \
"""Render ``add`` action.
"""

factory.defaults['array.remove'] = True
factory.doc['props']['array.remove'] = \
"""Render ``remove`` action.
"""

factory.defaults['array.sort'] = True
factory.doc['props']['array.sort'] = \
"""Render ``move up`` and ``move down`` actions.
"""
