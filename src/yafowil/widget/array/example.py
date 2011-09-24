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
    form = factory(
        u'form',
        name='example',
        props={'action': url})
    # array with leaf widgets
    form['myarray'] = factory(
        'array',
        props={'label': 'My Array'})
    form['myarray']['myfield'] = factory(
        'field:label:text',
        props={'label': 'My Field'})
    # array with compound widgets
    form['mycompoundarray'] = factory(
        'array',
        props={'label': 'My Compound Array'})
    form['mycompoundarray']['mycompound'] = factory('compound')
    form['mycompoundarray']['mycompound']['f1'] = factory(
        'field:label:text',
        props={'label': 'Field 1'})
    form['mycompoundarray']['mycompound']['f2'] = factory(
        'field:label:text',
        props={'label': 'Field 2'})
    # array with array widgets
    form['myarrayarray'] = factory(
        'array',
        props={'label': 'My Array Array'})
    form['myarrayarray']['myarray'] = factory(
        'array',
        props={'label': 'My Array'})
    form['myarrayarray']['myarray']['myfield'] = factory(
        'field:label:text',
        props={'label': 'My Field'})
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