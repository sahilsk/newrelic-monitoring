Newrelic Monitoring Setup
-------

This little project hellp you manage monitoring on newrelic i.e. add and update
newrelic monitoring, notification channels, and policies.

Currently it supports following newrelic monitoring
-------

- APM: Application monitoring via `apm_monitoring.py`


How-to
----

APM Monitoring
-----

- Create `application.json` file . Use `application.json.sample` for schema
  help.
- Create `.prod_monitring_env` file. Use `.prod_monitoring_env.sample` for
  schema help.
- lastly fire the script

```
cd  monitoring
./apm_monitoring.py
```


This will create newrelic application monitoring ( apdex, response time,
throughput, error-rate) using newrelic (new) alerts.


