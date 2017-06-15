""" Newrelic Application resource
"""

from newrelic import Newrelic


class Applications(Newrelic):

    def list(self, **kwargs):
        """
        Returns list of newrelic applications..

        :type kwargs: dict
        :param kwags: named argument: params, headers

        :rtype dict
        :return: The json of applications list filtered by payload
                 sent.

        ::
            {
                "applications": [
                    {
                        "name": "om-orchestrator-service-stg",
                        "language": "java",
                        "settings": {
                        ...
                        },
                        "reporting": true,
                        "application_summary": {
                            "host_count": 2,
                            "error_rate": 0.0,
                            "instance_count": 2,
                            ...
                        },
                        "links": {
                            "application_hosts": [
                               ...
                            ],
                            "alert_policy": 144407,
                            "application_instances": [
                                ...
                            ],
                            "servers": []
                        },
                        "health_status": "green",
                        "last_reported_at": "2017-06-08T18:28:35+00:00",
                        "id": 29862621
                    }
                ],
                "links": {
                    "application.servers": "/v2/servers?ids={server_ids}",
                    ...
                }
            }
        """
        rpath = "/applications.json"
        return self._get(
            self.getURL(rpath),
            params=kwargs.get('params', {}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def show(self, id, **kwargs):
        """
        Return applicaiton info identified by given id.

        :type id: int
        :param id: applicaiton id to find application

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: The json response of the api.
        """
        rpath = "/applications/%s.json" % id
        return self._get(
            self.getURL(rpath),
            params=kwargs.get('params', {}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def update(self, id, **kwargs):
        """
        Update application parameters and settings

        :type id: int
        :param id: application id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: json response of update request
        """
        rpath = "/applications/%s.json" % id
        return self._put(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {})),
            data={"application": kwargs.get('data', {})}
        )

    def delete(self, id, **kwargs):
        """
        Delete application along with its metrics

        :type id: int
        :param id: application id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: Json response of api
        """
        rpath = "/applications/%s.json" % id
        return self._delete(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )
