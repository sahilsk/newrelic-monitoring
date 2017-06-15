
""" Newrelic Alerts Conditions resource
"""

from newrelic import Newrelic
import json


class AlertsConditions(Newrelic):

    def list(self, id, **kwargs):
        """
        Returns list of newrelic alert policies.

        :type id: int
        :param id: policy id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype dict
        :return: The json of applications list filtered by payload
                 sent.

        """
        rpath = "/alerts_conditions.json"
        return self._get(
            self.getURL(rpath),
            params={'policy_id': id, 'page': kwargs.get('page', 0)},
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def create(self, id, **kwargs):
        """
        create new alert condition

        :type id: int
        :param id: policy id

        :type kwargs: dict
        :param kwags: named argument: headers, condition.
                      condition contain json

        :rtype: dict
        :return: The json response of the api.
        """
        rpath = "/alerts_conditions/policies/%s.json" % id
        condition = kwargs.get('condition')
        return self._post(
            self.getURL(rpath),
            data=json.dumps({"condition": condition}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def update(self, id, **kwargs):
        """
        Update alert condition parameters and settings

        :type id: int
        :param id: alert condition id

        :type kwargs: dict
        :param kwags: named argument: headers,condition
                      condition contain data to update

        :rtype: dict
        :return: json response of update request
        """
        rpath = "/alerts_conditions/%s.json" % id
        return self._put(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {})),
            data=json.dumps({"condition": kwargs.get('condition', {})})
        )

    def delete(self, id, **kwargs):
        """
        Delete alert condition

        :type id: int
        :param id: alert condition id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: Json response of api
        """
        rpath = "/alerts_conditions/%s.json" % id
        return self._delete(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )
