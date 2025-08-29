from typing import Any
from response import Response
from parse import parse
import types
import inspect

SUPPORTED_REQ_METHODS = {"GET", 'POST', 'DELETE'}

class NotSoFastAPI:
    def __init__(self, middlewares = [])->None:
        self.routes = dict()
        self.middlewares = middlewares
        self.route_middlewares = dict()
        

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
                    # print(self.routes)
                    for mw in self.route_middlewares[path][request_method]:
                        if isinstance(mw , types.FunctionType):
                            mw(environ)
                        else:
                            raise ValueError("you can only pass functions as middleware")
                    handler(environ, response,**res.named)
                    return response.as_wsgi(start_response)
        return response.as_wsgi(start_response)
                
                    

    def route_common(self,path, handler, method_name, middlewares):
        path_name = path or f"/{handler.__name__}"

        if path_name not in self.routes:
            self.routes[path_name]={}
            
        self.routes[path_name][method_name] = handler

        if path_name not in self.route_middlewares:
            self.route_middlewares[path_name] = {}
        self.route_middlewares[path_name][method_name] = middlewares

        return handler

    def get(self,path=None, middlewares = []):
        def wrapper(handler):
            return self.route_common(path, handler,'GET',middlewares)
            
        return wrapper

    def post(self, path=None, middlewares = []):
        def wrapper(handler):
            return self.route_common(path, handler, 'POST', middlewares)
        return wrapper

    def delete(self, path=None, middlewares = []):
        def wrapper(handler):
            return self.route_common(path, handler, 'DELETE',middlewares)
        return wrapper

    def route(self, path = None, middlewares = []):
        def wrapper(handler):
            if isinstance(handler, type):
                class_members = inspect.getmembers(handler, lambda x: inspect.isfunction(x) and not (
                    x.__name__.startswith("__") and x.__name__.endswith("__")
                    )  and x.__name__.upper() in SUPPORTED_REQ_METHODS)
                
                for fn_name, fn_handler in class_members:
                    self.route_common(path or f"/{handler.__name__}",fn_handler,fn_name.upper(), middlewares)

            else:
                raise ValueError("@route can be used only for classes")
        return wrapper