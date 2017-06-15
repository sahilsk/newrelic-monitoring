""" Newrelic **Alerts channels resource
"""

from newrelic import Newrelic
import json


class AlertsChannels(Newrelic):
    channel_list = []
    refresh = False

    def list(self, **kwargs):
        """
        Returns list of notification channels.

        :type kwargs: dict
        :param kwags: named argument: params, headers

        :rtype dict
        :return: The json of applications list filtered by payload
                 sent.
        """
        rpath = "/alerts_channels.json"
        return self._get(
            self.getURL(rpath),
            params=kwargs.get('params', {}),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def create(self, **kwargs):
        """
        create alert channel

        :type kwargs: dict
        :param kwags: named argument: headers, channel

        :rtype: dict
        :return: The json response of the api.
        """
        rpath = "/alerts_channels.json"
        payload = {
            "channel": {
                "name": kwargs.get('name'),
                "type": kwargs.get('type'),
                "configuration": kwargs.get('config')
            }
        }
        self.refresh = True
        return self._post(
            self.getURL(rpath),
            data=json.dumps(payload),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def delete(self, id, **kwargs):
        """
        Delete alert channel

        :type id: int
        :param id: channel id

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: Json response of api
        """
        rpath = "/alerts_channels/%s.json" % id
        self.refresh = True
        return self._delete(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {}))
        )

    def find(self, name, **kwargs):
        """
        Return matching channels identified by given name.
        As it loop through all pages, response is slow.

        :type name: string
        :param name: alert channels matching this name

        :type kwargs: dict
        :param kwargs: named argument: headers, refresh, type
                     :refresh: should refresh channel list
                     :type: channel type: slack, email pagerduty

        :rtype: dict
        :return: The json response of the api.
        """
        rpath = "/alerts_channels.json"
        refresh = kwargs.get("refresh", self.refresh)
        page = 1
        channel_type = kwargs.get('type')

        if len(self.channel_list) == 0:
            refresh = True

        while refresh:
            result = self._get(
                self.getURL(rpath),
                headers=self.getHeaders(kwargs.get('headers', {})),
                params="page=" + str(page)
            )
            channels = result.get('channels')
            if len(channels) == 0:
                break
            else:
                self.channel_list += channels
                page += 1
        self.refresh = False
        if channel_type is None:
            matching_alerts = filter(lambda x:
                                     x.get('name').lower() == name.lower(),
                                     self.channel_list)
        else:
            matching_alerts = filter(lambda x:
                                     x.get('name').lower() == name.lower() and
                                     x.get('type').lower() ==
                                     channel_type.lower(),
                                     self.channel_list)
        return matching_alerts
