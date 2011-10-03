import os
from yafowil import loader
import yafowil.webob
from yafowil.base import factory
from yafowil.controller import Controller
import yafowil.widget.array
from yafowil.tests import fxml
from webob import Request, Response

dir = os.path.dirname(__file__)


def javascript_response(environ, start_response):
    response = Response(content_type='text/javascript')
    with open(os.path.join(dir, 'resources', 'widget.js')) as js:
        response.write(js.read())
    return response(environ, start_response)


def css_response(environ, start_response):
    response = Response(content_type='text/css')
    with open(os.path.join(dir, 'resources', 'widget.css')) as js:
        response.write(js.read())
    return response(environ, start_response)


def img_response(environ, start_response):
    response = Response(content_type='image/png')    
    with open(os.path.join(dir, 'resources', 'images', 
                           environ['PATH_INFO'][8:])) as img:
        response.write(img.read())
    return response(environ, start_response)


def add_array_with_leafs(form):
    arr = form['somearray'] = factory(
        'array',
        value=['1', '2', '3'],
        props={
            'label': 'My Array',
        })
    arr['somefield'] = factory(
        'field:error:label:text',
        props={
            'label': 'Some Field',
            'required': 'Some Field is required',
        })


def add_array_with_compounds(form):
    arr = form['compoundarray'] = factory(
        'array',
        value=[
            {
                'f1': 'Value 1.1 F1',
                'f2': 'Value 1.2 F2',
            },
            {
                'f1': 'Value 2.1 F1',
                'f2': 'Value 2.2 F2',
            },
        ],
        props={
            'label': 'Compound Array',
        })
    comp = arr['somecompound'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'Field 1',
        })
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'Field 2',
            'required': 'Field 2 is required',
        })


def add_array_with_array_with_leafs(form):
    arr = form['arrayarray'] = factory(
        'array',
        value=[['1', '2'], ['3', '4'], ['5', '6']],
        props={
            'label': 'Array Array',
        })
    subarr = arr['somearray'] = factory(
        'array',
        props={
            'label': 'Some Array',
        })
    subarr['somefield'] = factory(
        'field:error:label:text',
        props={
            'label': 'Some Field',
            'required': 'Some Field is required',
        })


def add_array_with_array_with_compounds(form):
    arr = form['arrayarraycomp'] = factory(
        'array',
        value=[
            [
                {
                    'f1': 'Value 0.0 F1',
                    'f2': 'Value 0.0 F2',
                },
                {
                    'f1': 'Value 0.1 F1',
                    'f2': 'Value 0.1 F2',
                },
            ],
            [
                {
                    'f1': 'Value 1.0 F1',
                    'f2': 'Value 1.0 F2',
                },
                {
                    'f1': 'Value 1.1 F1',
                    'f2': 'Value 1.1 F2',
                },
            ],
        ],
        props={'label': 'Array 1'})
    subarr = arr['subarray'] = factory(
        'array',
        props={
            'label': 'Array 2',
        })
    comp = subarr['comp'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'F1',
        })
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'F2',
            'required': 'F2 is required',
        })


def add_array_with_array_with_array_with_leafs(form):
    arr_1 = form['array_1'] = factory(
        'array',
        value=[
            [
                ['1', '2'],
                ['3'],
            ],
            [
                ['4', '5'],
            ],
        ],
        props={
            'label': 'Array 1',
        })
    arr_2 = arr_1['array_2'] = factory(
        'array',
        props={
            'label': 'Array 2',
        })
    arr_3 = arr_2['array_3'] = factory(
        'array',
        props={
            'label': 'Array 3',
        })
    arr_3['textfield'] = factory(
        'field:error:label:text',
        props={
            'label': 'Text Field',
            'required': 'Text Field is required',
        })


def add_array_with_array_with_array_with_compounds(form):
    arr_1 = form['comp_array_1'] = factory(
        'array',
        value=[
            [
                [
                    {
                        'f1': 'Value F1',
                        'f2': 'Value F2',
                    },
                ],
            ],
            [
                [
                    {
                        'f1': 'Value F1',
                        'f2': 'Value F2',
                    },
                ],
            ],
        ],
        props={
            'label': 'Array 1',
        })
    arr_2 = arr_1['array_2'] = factory(
        'array',
        props={
            'label': 'Array 2',
        })
    arr_3 = arr_2['array_3'] = factory(
        'array',
        props={
            'label': 'Array 3',
        })
    comp = arr_3['comp'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'F1',
        })
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'F2',
            'required': 'F2 is required',
        })


def app(environ, start_response):
    url = 'http://%s/' % environ['HTTP_HOST']
    if environ['PATH_INFO'] == '/ywa.js':
        return javascript_response(environ, start_response)
    elif environ['PATH_INFO'] == '/ywa.css':
        return css_response(environ, start_response)
    elif environ['PATH_INFO'].startswith('/images/'):
        return img_response(environ, start_response)
    elif environ['PATH_INFO'] != '/':
        response = Response(status=404)
        return response(environ, start_response)
    
    form = factory(u'form', name='example', props={'action': url})
    
    add_array_with_leafs(form)
    add_array_with_compounds(form)
    add_array_with_array_with_leafs(form)
    add_array_with_array_with_compounds(form)
    add_array_with_array_with_array_with_leafs(form)
    add_array_with_array_with_array_with_compounds(form)
    
    form['submit'] = factory(
        'field:submit',
        props={        
            'label': 'submit',
            'action': 'save',
            'handler': lambda widget, data: None,
            'next': lambda request: url})
    
    controller = Controller(form, Request(environ))
    tag = controller.data.tag
    jq = tag('script', ' ',
             src='https://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.js',
             type='text/javascript')
    ywd = tag('script', ' ',
              src='%sywa.js' % url,
              type='text/javascript')
    css = tag('style',
              '@import url(%sywa.css)' % url,
              type='text/css')
    head = tag('head', jq, ywd, css)
    h1 = tag('h1', 'YAFOWIL Widget Array Example')
    body = tag('body', h1, controller.rendered)
    response = Response(body=fxml(tag('html', head, body)))
    return response(environ, start_response)