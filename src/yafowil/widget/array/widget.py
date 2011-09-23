#from odict import odict
from yafowil.base import (
    UNSET,
    factory,
    ExtractionError,
    fetch_value
)
from yafowil.utils import (
    cssid,
    cssclasses,
    css_managed_props,
    managedprops,
)
from yafowil.compound import (
    compound_extractor,
    compound_renderer,
)


def actions_renderer(widget, data):
    tag = data.tag
    actions = list()
    for key in ['add', 'remove', 'up', 'down']:
        if widget.attrs.get(key):
            class_ = 'array_row_%s' % key
            action = tag('a', '&#160;', href='#', class_=class_)
            actions.append(action)
    kw = dict(class_='array_actions')
    return tag('div', *actions, **kw)


factory.register(
    'array_actions',
    edit_renderers=[actions_renderer])

# dont document internal widget
factory.doc['blueprint']['array_actions'] = UNSET


def array_builder(widget, factory):
    table = widget['table'] = factory('table', props={'structural': True})
    head = table['head'] = factory('thead', props={'structural': True})
    row = head['row'] = factory('tr', props={'structural': True})
    row['_'] = factory(
        'th',
        props = {
            'structural': True,
            'label': u' ',
        }
    )
    if not widget.attrs['static']:
        row['actions'] = factory(
            'th:array_actions',
            props = {
                'structural': True,
                'add': True,
            }
        )
    table['body'] = factory('tbody', props={'structural': True})


@managedprops('array', *css_managed_props)
def array_wrapper_renderer(widget, data):
    kw = {
        'id': cssid(widget, 'array'),
        'class': cssclasses(widget, data),
    }
    rendered = data.rendered
    return data.tag('div', rendered, **kw)


def array_edit_renderer(widget, data):
    if len(widget) == 1 and not widget.has_key('TEMPLATE_CONTAINER'):
        raise Exception(u"Empty array widget defined")
    if not widget.has_key('TEMPLATE_CONTAINER'):
        container = widget['container'] = factory(
            'div',
            props={
                'structural': True,
                'class': 'arraytemplate',
            })
        template = widget.detach(widget.keys()[1])
        if template.attrs.get('structural'):
            raise Exception(u"Compound templates for arrays must not be "
                            u"structural.")
        container['TEMPLATE'] = template
    
    # XXX: value extraction
    
    #import pdb;pdb.set_trace()

#    static = widget.attrs['static']
#    table = widget['table']
#    table.attrs['id'] = 'dictwidget_%s.entry' % widget.dottedpath
#    body = table['body']
#    body.clear()
#    if data.errors and static:
#        basename = '%s.entry' % body.dottedpath
#        value = extract_static(data, basename)
#    else:
#        value = fetch_value(widget, data)
#    if not value:
#        return
#    i = 0
#    for key, val in value.items():
#        row = body['entry%i' % i] = factory('tr')
#        k_props = {'class': 'key'}
#        if static:
#            k_props['disabled'] = 'disabled'
#        row['key'] = factory(
#            'td:text',
#            value = key,
#            name = 'key',
#            props = k_props,
#        )
#        row['value'] = factory(
#            'td:text',
#            value = val,
#            name = 'value',
#            props = {
#                'class': 'value',
#            },
#        )
#        if not static:
#            row['actions'] = factory(
#                'td:dict_actions',
#                props = {
#                    'add': True,
#                    'remove': True,
#                    'up': True,
#                    'down': True,
#                },
#            )
#        i += 1


#def raise_extraction_error(widget):
#    if isinstance(widget.attrs['required'], basestring):
#        raise ExtractionError(widget.attrs['required'])
#    raise ExtractionError(widget.attrs['required_message'])


#def extract_static(data, basename):
#    request = data.request
#    ret = odict()
#    index = 0
#    keys = data.value.keys()
#    while True:
#        valuename = '%s%i.value' % (basename, index)
#        if request.has_key(valuename):
#            if index >= len(keys):
#                raise ExtractionError('invalid number of static values')
#            ret[keys[index]] = request[valuename]
#            index += 1
#            continue
#        break
#    return ret


#def extract_dynamic(data, basename):
#    request = data.request
#    ret = odict()
#    index = 0
#    while True:
#        keyname = '%s%i.key' % (basename, index)
#        valuename = '%s%i.value' % (basename, index)
#        if request.has_key(keyname):
#            key = request[keyname].strip()
#            if key:
#                ret[key] = request[valuename]
#            index += 1
#            continue
#        break
#    return ret


#def dict_extractor(widget, data):
#    static = widget.attrs['static']
#    body = widget['table']['body']
#    basename = '%s.entry' % body.dottedpath
#    req = data.request
#    index = 0
#    if static:
#        ret = extract_static(data, basename)
#    else:
#        ret = extract_dynamic(data, basename)
#    if len(ret) == 0:
#        ret = UNSET
#    if widget.attrs.get('required'):
#        if ret is UNSET:
#            raise_extraction_error(widget)
#        if static:
#            for val in ret.values():
#                if not val:
#                    raise_extraction_error(widget)
#    return ret


def array_display_renderer(widget, data):
    return '<div>Array display</div>'

#    value = data.value
#    if not value:
#        value = dict()
#    values = list()
#    for key, val in value.items():
#        values.append(data.tag('dt', key) + data.tag('dd', val))
#    head = u''
#    if widget.attrs.get('head'):
#        head = '%s: %s' % (widget.attrs['head']['key'],
#                           widget.attrs['head']['value'])
#        head = data.tag('h5', head)
#    return head + data.tag('dl', *values)


factory.register(
    'array',
    extractors=[compound_extractor],
    edit_renderers=[array_edit_renderer, compound_renderer, array_wrapper_renderer],
    display_renderers=[array_display_renderer],
    builders=[array_builder])

factory.doc['blueprint']['array'] = \
"""Add-on widget `yafowil.widget.array 
<http://github.com/bluedynamics/yafowil.widget.array/>`_.
"""

factory.defaults['array.class'] = 'array'

factory.defaults['array.static'] = False

factory.defaults['array.error_class'] = 'error'

factory.defaults['array.message_class'] = 'errormessage'