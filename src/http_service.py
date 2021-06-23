#!/usr/bin/env python3
import requests
import functools
import json

ENABLE_DEBUG = False


def log_response(response):
    print("Response CODE:", response.status_code)
    print("Response TEXT:", response.text)
    print("Response DATA:", json.dumps(
        response.json(), indent=3, sort_keys=True))


def error_handler(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)

            return result
        except Exception as e:
            print("Request failed: ", e)

    return wrap


def logger(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        response = func(self, *args, **kwargs)

        if ENABLE_DEBUG:
            log_response(response)

        return response

    return wrap


class HTTP:
    DOMAIN = 'api.hibob.com'
    API_PATH = 'api'

    def __init__(self, https=True, debug=False):
        self.debug = debug
        self.session = self.get_session()
        self.BASE_URL = f"{'https' if https else 'http'}://{self.DOMAIN}/{self.API_PATH}"

    def get_session(self):
        return requests.Session()

    @error_handler
    @logger
    def POST(self, path, payload={}):
        response = self.session.post(self.BASE_URL + path,
                                     json=payload)
        return response

    @error_handler
    @logger
    def PUT(self, path, payload={}):
        response = self.session.put(self.BASE_URL + path,
                                    json=payload)
        return response

    @error_handler
    @logger
    def GET(self, path, params=None):
        response = self.session.get(
            self.BASE_URL + path, params=params)
        return response
