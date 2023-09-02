import requests
from requests import HTTPError
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
    def handle_response(response):
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(f"HTTP Error occurred: {http_err}")
            raise
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            raise
        logger.info(f"Response:\n{response.json}")
        return response.json()

    def send_request(self, url, method='GET', data=None):
        methods = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }
        if method not in methods:
            logger.error("Invalid method")
            return
        logger.info(f"sent request URL-{url}  method-{method}")
        response = methods[method](url, auth=HTTPBasicAuth(self.username, self.password), json=data)
        return self.handle_response(response)

