from flask import request
from werkzeug.wrappers import Request, Response, ResponseStream
from flask_restful import Resource, reqparse
from functools import wraps
from io import BytesIO


def print_data(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.args.get('text')

        print("====================================", token)
        #data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        #print(data)
        return func()
    return decorator

class middleware():
    #@print_data

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        #@wraps(self, environ, start_response)
        #def decorator(*args, **kwargs):
            #length = int(environ.get('CONTENT_LENGTH') or 0)
            #body = environ['wsgi.input'].read(length)
            #environ['body_copy'] = body
            request = Request(environ)


            # replace the stream since it was exhausted by read()

            #print('url: %s, path: %s' % ( request.url, request.path))
            print('---------------------------------------------------------------------------------------')

            print(request.method)

            print(request.origin)

            if request.method == 'POST':
                print(request.data)
                print(dir(request))
                #print(request.args['text'])
            #    data = request.form.copy()
            #    print(data)

            print(request.host)
            #environ['wsgi.input'] = BytesIO(body)
            print('-------------------xxxxx----------------')

            return self.app( environ, start_response)
        #return decorator
