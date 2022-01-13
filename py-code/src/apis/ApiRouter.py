
from typing import Callable, Mapping
from types import MappingProxyType
import re


class ApiRouteError(Exception):
    def __init__(self, *args, **kwargs):
        super(ApiRouteError, self).__init__(*args, **kwargs)


class ApiRouter:
    """
    ApiRouter is singleton so it can be instantiated safely in different modules
    """
    __instance = None
    __mapping = {}

    mapping = MappingProxyType(__mapping)
    
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __check_route_format(self, route):
        if not isinstance(route, str):
            raise TypeError('parameter route should be str')
        RE = '(:[a-zA-Z][\w\-]*\w)*'
        if not re.fullmatch(RE, route):
            raise ValueError('Invalid route format. Regular expression: {}'.format(RE))

    def list_apis(self):
        return sorted(self.mapping.keys())

    def route(self, route):
        """
        decorator, register the decorated function to ApiRouter
        """
        def decorator(func):
            self.register(route, func)
            return func
        return decorator

    def register(self, route, method: Callable):
        self.__check_route_format(route)
        if not callable(method):
            raise TypeError('parameter method should be callable')
        if route in self.mapping:
            raise KeyError('route {} has already been registered. you should delete it before re-register.')
        self.__mapping[route] = method

    def delete(self, route):
        self.__mapping.pop(route)

    def register_from_map(self, api_map: Mapping):
        for route, method in api_map.items():
            self.register(route, method)

    def invoke_api(self, route, args=[], kwargs={}):
        if route == ':':
            # root route is reserved for listing api routes
            reply = self.list_apis()
        else:
            try:
                _method = self.mapping[route]
            except KeyError:
                raise ApiRouteError('route does not exist: {}'.format(route))
            reply = _method(*args, **kwargs)
        return reply
