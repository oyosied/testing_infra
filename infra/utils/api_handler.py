import urllib
from json import JSONDecodeError
from typing import Dict

import requests
from requests import HTTPError, Response
from requests.auth import HTTPBasicAuth
from loguru import logger

"""
I'd prefer using an API client such as autorest - http://azure.github.io/autorest/generate/
as it'll much easier use and you don't need to handle rest response and structure
"""


class ApiHandler:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def handle_response(response: Response,pass_on_error):
        data = ''
        try:
            response.raise_for_status()
            if response.content:
                try:
                    data = response.json()
                except JSONDecodeError:
                    print("JSONDecodeError: Couldn't decode the response.")

        except HTTPError as http_err:
            logger.error(f"HTTP Error occurred: {http_err}")
            logger.error(f"Error Response: {response.content.decode('utf-8')}")
            if pass_on_error:
                return data
            raise
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            if pass_on_error:
                return data
            raise
        logger.info(f"Response:\n{data}")
        return data

    def send_request(self, url, method='GET', data: Dict=None, params=None, pass_on_error: bool=False) -> Dict:
        methods = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }
        if method not in methods:
            logger.error("Invalid method")
            return
        logger.info(f"Sent request URL-{url}  method-{method}  data-{data}  params-{params}")

        if params is not None:
            params = urllib.parse.urlencode(params, safe=':+')

        response = methods[method](
            url,
            auth=HTTPBasicAuth(self.username, self.password),
            json=data,
            params=params
        )
        return self.handle_response(response=response,pass_on_error=pass_on_error)


