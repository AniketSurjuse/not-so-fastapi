from typing import Any
from response import Response
from parse import parse
import types
class NotSoFastAPI:

    def __init__(self, middlewares = [])->None:
        self.routes = dict()
        self.middlewares = middlewares

    def __call__(self, environ, start_response)->Any:
        path_name = environ["PATH_INFO"]
        method = environ["REQUEST_METHOD"]
        response = Response()
        for middleware in self.middlewares:
            if isinstance(middleware , types.FunctionType):
                middleware(environ)
            else:
                raise ValueError("you can only pass functions as middleware")
        for path, handler_dict in self.routes.items():
            res = parse(path, environ['PATH_INFO'])
            #res is empty if path matches but no slug found, dict if slug found and none if path doesn't matches.
            for request_method, handler in handler_dict.items():
                if request_method==method and res:
                    handler(environ, response,**res.named)
                    return response.as_wsgi(start_response)
        return response.as_wsgi(start_response)
                
                    

    def route_common(self,path, handler, method_name):
        path_name = path or f"/{handler.__name__}"
        if path_name not in self.routes:
            self.routes[path_name]={}
            
        self.routes[path_name][method_name] = handler

    def get(self,path=None):
        def wrapper(handler):
            self.route_common(path, handler,'GET')
            
        return wrapper

    def post(self, path=None):
        def wrapper(handler):
            self.route_common(path, handler, 'POST')
        return wrapper

    def delete(self, path=None):
        def wrapper(handler):
            self.route_common(path, handler, 'DELETE')
        return wrapper