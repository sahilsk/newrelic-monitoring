""" Newrelic Notification channels resource
"""

from newrelic import Newrelic


class NotificationChannels(Newrelic):

    def list(self, **kwargs):
        """
        Returns list of notification channels.

        :type kwargs: dict
        :param kwags: named argument: params, headers

        :rtype dict
        :return: The json of applications list filtered by payload
                 sent.
        """
        rpath = "/notification_channels.json"
        return self._get(
            self.getURL(rpath),
            params=kwargs.get('params', {}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def show(self, id, **kwargs):
        """
        Return channel info identified by given id.

        :type id: int
        :param id: channel id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: The json response of the api.
        """
        rpath = "/notification_channels/%s.json" % id
        return self._get(
            self.getURL(rpath),
            params=kwargs.get('params', {}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

