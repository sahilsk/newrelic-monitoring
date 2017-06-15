""" Newrelic Alerts Conditions resource
"""

from newrelic import Newrelic
import json


class AlertsPolicyChannels(Newrelic):
    def update(self, policy_id, channel_ids, **kwargs):
        """
        Update alert condition parameters and settings

        :type policy_id: int
        :param policy_id: policy id to associate channels with.

        :type channel_ids: int array
        :param channel_ids: array of ids to associate with a policy.

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: json response of update request
        """
        rpath = "/alerts_policy_channels.json"
        channel_ids = ','.join(map(lambda x: str(x), channel_ids))
        payload = {
            "policy_id": policy_id,
            "channel_ids": channel_ids
        }
        return self._put(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {})),
            data=json.dumps(payload)
        )

    def delete(self, policy_id, channel_id, **kwargs):
        """
        Delete alert policy and channel association.

        :type policy_id: int
        :param policy_id: policy id to associated with channel

        :type channel_id: int
        :param channel_id: channel id to disassociate

        :type kwargs: dict
        :param kwags: named argument: headers

        :rtype: dict
        :return: Json response of api
        """
        rpath = "/alerts_conditions/%s.json" % id
        payload = {
            "policy_id": policy_id,
            "channel_id": channel_id
        }
        return self._delete(
            self.getURL(rpath),
            headers=self.getHeaders(kwargs.get('headers', {})),
            data=payload
        )
