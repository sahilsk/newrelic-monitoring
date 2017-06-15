""" Newrelic Alert policies resource
"""

from newrelic import Newrelic
import json


class AlertsPolicies(Newrelic):

    def list(self, **kwargs):
        """
        Returns list of newrelic alert policies.

        :type kwargs: dict
        :param kwags: named argument: params, headers

        :rtype dict
        :return: The json of applications list filtered by payload
                 sent.

        ::
        """
        rpath = "/alerts_policies.json"
        return self._get(
            self.getURL(rpath),
            params=kwargs.get('params', {}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def create(self, **kwargs):
        """
        create alert policy

        :type kwargs: dict
        :param kwags: named argument: headers, policy.
                      policy contain json for policy creation

        :rtype: dict
        :return: The json response of the api.
        """
        rpath = "/alerts_policies.json"
        return self._post(
            self.getURL(rpath),
            data=json.dumps(kwargs.get('policy')),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def update(self, id, **kwargs):
        """
        Update application parameters and settings

        :type id: int
        :param id: policy id

        :type kwargs: dict
        :param kwags: named argument: headers, policy
                      policy contain data to update

        :rtype: dict
        :return: json response of update request
        """
        rpath = "/alerts_policies/%s.json" % id
        return self._put(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {})),
            data=json.dumps(kwargs.get('policy', {}))
        )

    def delete(self, id, **kwargs):
        """
        Delete alert policy

        :type id: int
        :param id: alert policy id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: Json response of api
        """
        rpath = "/alerts_policies/%s.json" % id
        return self._delete(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )
