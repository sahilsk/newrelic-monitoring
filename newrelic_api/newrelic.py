""" newrelic base class

"""
import requests


class Newrelic(object):
    """ initialize newrelic client """

    base_url = "https://api.newrelic.com"
    api_version = "v2"
    api_key = None
    client_name = "newrelic-api-py"

    def getURL(self, rpath):
        return self.base_url + "/" + self.api_version\
                + rpath

    def getHeaders(self, extra_headers={}):
        defaultHeaders = {
            'api-client-name': self.client_name,
            'X-Api-Key': self.api_key,
            'content-type': 'application/json'
        }
        return dict(defaultHeaders.items() + extra_headers.items())

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is None:
            raise "api key not entered"

    def _get(self, *args, **kwargs):
        url = args[0]
        response = requests.get(url,
                                headers=kwargs['headers'],
                                params=kwargs['params']
                                )
        if not response.ok:
            raise Exception("{}:{}".format(response.status_code,
                                           response.text))
        return response.json()

    def _post(self, *args, **kwargs):
        url = args[0]
        response = requests.post(url,
                                 headers=kwargs['headers'],
                                 data=kwargs['data']
                                 )
        if not response.ok:
            raise Exception("{}:{}".format(response.status_code,
                                           response.text))
        return response.json()

    def _put(self, *args, **kwargs):
        url = args[0]
        response = requests.put(url,
                                headers=kwargs['headers'],
                                data=kwargs['data']
                                )
        if not response.ok:
            raise Exception("{}:{}".format(response.status_code,
                                           response.text))
        return response.json()

    def _delete(self, *args, **kwargs):
        url = args[0]
        response = requests.delete(url,
                                   headers=kwargs['headers'],
                                   data=kwargs.get('data')
                                   )
        if not response.ok:
            raise Exception("{}:{}".format(response.status_code,
                                           response.text))
        return response.json()
