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
    
    # create form
    form = factory(u'form', name='example', props={'action': url})
    
    # array with leaf widgets
    arr = form['myarray'] = factory(
        'array',
        value=['1', '2', '3'],
        props={'label': 'My Array'})
    arr['myfield'] = factory(
        'field:error:label:text',
        props={
            'label': 'My Field',
            'required': 'Field must not be empty',
        })
    
    # array with compound widgets
    cparr = form['mycompoundarray'] = factory(
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
            'label': 'My Compound Array',
        })
    comp = cparr['mycompound'] = factory('compound')
    comp['f1'] = factory('field:label:text', props={'label': 'Field 1'})
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'Field 2',
            'required': 'Field 2 is required',
        })
    
    # array with array widgets
    arrarr = form['myarrayarray'] = factory(
        'array',
        value=[['1', '2'], ['3', '4'], ['5', '6']],
        props={
            'label': 'My Array Array',
        })
    arr = arrarr['myarray'] = factory(
        'array',
        props={
            'label': 'My Array',
        })
    arr['myfield'] = factory(
        'field:error:label:text',
        props={
            'label': 'My Field',
            'required': 'My Field is required',
        })
    
    # array widget with array with compound
    arr = form['myarrayarraycomp'] = factory(
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
        props={'label': 'My Compound Array'})
    subarr = arr['subarray'] = factory(
        'array',
        props={
            'label': 'Subarray',
        })
    comp = subarr['mycompound'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'F1',
        })
    comp['f2'] = factory(
        'field:label:text',
        props={
            'label': 'F2',
        })
    
#    # 3-dimensional array
#    _3darr = form['my3dimensional'] = factory(
#        'array',
#        value=[
#            # 1
#            [   
#                #2
#                [
#                    {
#                        'mycompound.f1': 'F 1',
#                        'mycompound.f2': 'F 2',
#                    },
#                ],
#            ],
#        ],
#        props={
#            'label': 'My 3 Dimensional Array',
#        })
#    arrarr = _3darr['myarrayarray'] = factory(
#        'array',
#        props={
#            'label': 'My Array Array',
#        })
#    arr = arrarr['myarray'] = factory(
#        'array',
#        props={
#            'label': 'My Array',
#        })
#    comp = arr['mycompound'] = factory('compound')
#    comp['f1'] = factory(
#        'field:error:label:text',
#        props={
#            'label': 'Field 1',
#            'required': 'Field 1 is required',
#        })
#    comp['f2'] = factory(
#        'field:label:text',
#        props={
#            'label': 'Field 2',
#        })
    
    # submit action
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