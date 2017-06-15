#!/usr/bin/env python
import sys
sys.path.append('../')

from newrelic_api.alerts_channels import AlertsChannels
from newrelic_api.applications import Applications
from newrelic_api.alerts_policies import AlertsPolicies
from newrelic_api.alerts_conditions import AlertsConditions
from newrelic_api.alerts_policy_channels import AlertsPolicyChannels

import json

app_config = json.load(open('.prod_monitoring_env'))
nChannels = AlertsChannels(app_config.get('newrelic'))
nPolicyChannels = AlertsPolicyChannels(app_config.get('newrelic'))
nApps = Applications(app_config.get('newrelic'))
nPolicy = AlertsPolicies(app_config.get('newrelic'))
nCondition = AlertsConditions(app_config.get('newrelic'))


metric_matrix = {
    "response_time_web": "Response time (web)",
    "apdex": "Apdex",
    "error_percentage": "Error percentage",
    "throughput_web": "Throughput (web)",
}


def create_channel(data, type):
    if type == "email":
        channel_name = data
        channel_type = "email"
        config = {
                "recipients": data,
                "include_json_attachment": False
                }
    elif type == "pagerduty":
        channel_name = data
        channel_type = "pagerduty"
        config = {
                "service_key": app_config['pagerduty'][data]
                }
    elif type == "slack":
        channel_name = data
        channel_type = "slack"
        config = {
                "channel": data,
                "url": app_config['slack'][data]
                }
    result = nChannels.create(name=channel_name, type=channel_type,
                              config=config)
    print result


def update_condition(condition, app_id, metric, config):
    if app_id is None:
        raise Exception("Application id can't be none")
    g_condition = {
              "type": "apm_app_metric",
              "name": metric_matrix[metric],
              "enabled": config.get('enable', True),
              "entities": [app_id],
              "metric": metric,
              "condition_scope": "application",
              "terms": []
            }
    if config.get('operator', 'above') == "above":
        g_condition['name'] += " (High)"
    else:
        g_condition['name'] += " (Low)"

    c_critical = config.get('critical')
    if c_critical:
        c_term = {
            "duration": c_critical['duration'],
            "operator": config.get('operator', "above"),
            "priority": "critical",
            "threshold": c_critical['threshold'],
            "time_function": "all"
        }
        g_condition['terms'].append(c_term)

    c_warning = config.get('warning')
    if config.get('warning'):
        w_term = {
            "duration": c_warning['duration'],
            "operator": config.get('operator', "above"),
            "priority": "warning",
            "threshold": c_warning['threshold'],
            "time_function": "all"
        }
        g_condition['terms'].append(w_term)
    nCondition.update(condition['id'], condition=g_condition)


def create_condition(policy_id, app_id, metric, config):
    """
    Create condtion under policy.

    It uses convention for naming condition

    Apdex (Low): for apdex condition
    Error percentage (High): for high error rate
    Throughput (web) (High): for high web throughput
    metric: when apm_app_metric: apdex, error_percentage,
           response_time_web, response_time_background,
           throughput_web, throughput_background, user_defined.
    """
    if app_id is None:
        raise Exception("Application id can't be none")
    if policy_id is None:
        raise Exception("policy id can't be none")

    print policy_id
    g_condition = {
              "type": "apm_app_metric",
              "name": metric_matrix[metric],
              "enabled": config.get('enable', True),
              "entities": [app_id],
              "metric": metric,
              "condition_scope": "application",
              "terms": []
            }
    if config.get('operator', 'above') == "above":
        g_condition['name'] += " (High)"
    else:
        g_condition['name'] += " (Low)"

    c_critical = config.get('critical')
    if c_critical:
        c_term = {
            "duration": c_critical['duration'],
            "operator": config.get('operator', "above"),
            "priority": "critical",
            "threshold": c_critical['threshold'],
            "time_function": "all"
        }
        g_condition['terms'].append(c_term)

    c_warning = config.get('warning')
    if config.get('warning'):
        w_term = {
            "duration": c_warning['duration'],
            "operator": config.get('operator', "above"),
            "priority": "warning",
            "threshold": c_warning['threshold'],
            "time_function": "all"
        }
        g_condition['terms'].append(w_term)

    result = nCondition.create(policy_id,
                               condition=g_condition)
    print result


def ensure_conditions(policy_id, app_id, checks):
    existing_conditions = nCondition.list(policy_id).get('conditions', [])
    for key, configs in checks.items():
        metric_name = metric_matrix[key]
        for config in configs:
            if config.get('operator', 'above') == "above":
                condition_name = metric_name + " (High)"
            else:
                condition_name = metric_name + " (Low)"
            c_data = filter(lambda x: x['name'].lower() ==
                            condition_name.lower(),
                            existing_conditions)
            if len(c_data) == 0:
                print "creating-" + condition_name
                create_condition(policy_id, app_id, key, config)
            else:
                print "updating-" + condition_name
                update_condition(c_data[0], app_id, key, config)


def attach_channels(policy, channels):
    channel_ids = map(lambda x:  x.get('id'), channels)
    nPolicyChannels.update(policy.get('id'), channel_ids)


def ensure_email_channels(emails):
    channels = []
    for email in emails:
        filter_channels = nChannels.find(email, type='email', refresh=False)
        if len(filter_channels) == 0:
            print "creating email channel: %s" % email
            channels += create_channel(email, type='email')
        else:
            channels.append(filter_channels[0])
    return channels


def ensure_pagerduty_channels(pagerdutys):
    channels = []
    for pagerduty in pagerdutys:
        filter_channels = nChannels.find(pagerduty, type='pagerduty')
        if len(filter_channels) == 0:
            create_channel(pagerduty, type='pagerduty')
        else:
            channels.append(filter_channels[0])
    return channels


def ensure_slack_channels(slacks):
    channels = []
    for slack in slacks:
        filter_channels = nChannels.find(slack, type='slack')
        if len(filter_channels) == 0:
            create_channel(slack, type='slack')
        else:
            channels.append(filter_channels[0])
    return channels


def ensure_channels(app_name, alert_channels):
    channels = []
    if alert_channels is None:
        return None
    channels += ensure_email_channels(alert_channels.get('email'))
    channels += ensure_pagerduty_channels(alert_channels.get('pagerduty'))
    channels += ensure_slack_channels(alert_channels.get('slack'))
    return channels


def ensure_alert_policy(name):
    policies = nPolicy.list(params={
        "filter[name]": name
    })
    if len(policies.get('policies')) == 0:
        policy = {
              "policy": {
                      "incident_preference": "PER_POLICY",
                      "name": name
                    }
        }
        app_policy = nPolicy.create(policy=policy).get('policy')
    else:
        app_policy = policies.get('policies')[0]
    return app_policy


def print_obj(obj):
    print json.dumps(obj, indent=4)


def process_app(app):
    app_name = app.get('name')
    filterApps = nApps.list(params={
        "filter[name]": app_name
    })
    if len(filterApps['applications']) == 0:
        raise Exception("Application(%s) doesn't exist" % app_name)
    application = filterApps['applications'][0]
    policy = ensure_alert_policy(app_name)
    channels = ensure_channels(app_name, app.get('alert_channels'))
    attach_channels(policy, channels)
    ensure_conditions(policy['id'], application['id'],
                      app.get('checks'))


if __name__ == "__main__":
    fapps = json.load(open("applications.json"))
    for app in fapps['applications']:
        process_app(app)
