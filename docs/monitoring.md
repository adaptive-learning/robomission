# Monitoring

| Dashboard | <https://robomise.cz/monitoring> |
| --------- | -------------------------------- |

Even with careful testing,
there will always be some errors in the deployed system.
Monitoring tools help to spot these errors quickly
and provide us with a good guide on what we should improve
in next iterations.

## Monitoring Services Overview

| Service | Code | Logs |
| ------- | ---- | ---- |
| [Dashboard]           | [MonitoringPage.jsx] | |
| [Monitoring Notebook] | [monitoring_template.ipynb] | |
| [DB Admin]            | [admin.py] | |
| [Metrics]             | [metrics.py] | management.log |
| [Errors]              | [settings.py]<sup>\*</sup> | robomission.log |
| [Feedback]            | [feedback.py] | feedback.log |
| [Google Analytics]    | [googleAnalytics.js] | |

<sup>\*</sup> Related options in `settings.py` are ADMIN and LOGGING.


## Metrics

* All metrics are stored in a single DB table ([monitoring.models.Metric][models.py]).
* They are defined in [metrics.py].
* Recent metrics are visualized in [the monitoring dashboard][Dashboard].
* Metrics recomputed every night using cron. (details: [cronjobs.md](./cronjobs.md))

## Monitoring Notebook

* Performs basic analyses of collected data.
* Recomputed every week by cron. (details: [cronjobs.md](./cronjobs.md))
* Available at: <https://robomise.cz/media/exports/monitoring_latest.html>.
* To extend the analysis, simply edit [monitoring_template.ipynb].


## Google Analytics

* [Google Analytics - Romobission](https://analytics.google.com/analytics/web/#embed/report-home/a81667720w121094822p126691725/)
* [googleAnalytics.js] - defines all messages sent to Google Analytics.
* You can set sending reports by email (e.g. weekly).


## Error Reports

Unhandled exceptions on the server are
logged to `robomission.log`
and sent to <adaptive-programming-errors@googlegroups.com>.
You can subscribe to
[adaptive-programming-errors google group](https://groups.google.com/forum/#!forum/adaptive-programming-errors)
to receive emails about the unhandled exceptions.
In the [settings for your groups](https://groups.google.com/forum/#!myforums)
you can set frequency of reports to "daily summary"
to make sure that you will receive at most 1 email per day.
(Sending every new message is potentially dangerous.)


## User Feedback

Feedback from users are logged to `feedback.log`
and sent to <adaptive-programming@googlegroups.com>.
You can subscribe to
[adaptive-programming google group](https://groups.google.com/forum/#!forum/adaptive-programming)
to receive an email for each new feedback.


## Data Investigation

All collected data are exported once a week
(details: [cronjobs.md](./cronjobs.md)).
To download the collected data and perform an analysis without this repo,
follow the instructions in [//docs/data.md](./data.md).

However, the `monitoring` app in this repo makes the data investigation simpler
by providing prepared jupyter notebooks and helper functions,
such as `get_production_data(datestamp)`,
that fetches collected data from the production system,
stores them in local cache (`//.prodcache/robomission-[datestamp]`),
and returns a dictionary of dataframes with the data.

Prepared Jupyter notebooks:
* [investigation_template.ipynb] – with just imports and data loading,
* [monitoring_template.ipynb] – with weekly-performed analyses,
* [branch:monitoring//backend/monitoring/notebooks/](https://github.com/adaptive-learning/robomission/tree/monitoring/backend/monitoring/notebooks) – all notebooks.

To run Jupyter with Django kernel, use:
```
make notebook
```

You can either start a new notebook,
or you can make a copy of an existing notebook (`File > Make a Copy`).
Always create notebooks inside the dedicated `monitoring` branch
and store them at:
```
//backend/monitoring/notebooks/investigation_<datestamp>_<name>.ipynb
```
Pushing a notebook to the remote-tracking branch on GitHub
allows you to send a link to the investigation
(and GitHub generates previews of jupyter notebooks).

There is a shortcut:
```
make investigation
```
It switches to the `monitoring` branch,
creates a new jupyter notebook from the [investigation_template.ipynb],
and opens it in the browser.


[Dashboard]: https://robomise.cz/monitoring
[MonitoringPage.jsx]: ../frontend/src/components/MonitoringPage.jsx
[Metrics]: https://robomise.cz/admin/monitoring/metric/
[metrics.py]: ../backend/monitoring/metrics.py
[DB Admin]: https://robomise.cz/admin/
[admin.py]: ../backend/learn/admin.py
[Errors]: https://groups.google.com/forum/#!forum/adaptive-programming-errors
[settings.py]: ../backend/robomission/settings.py
[Feedback]: https://groups.google.com/forum/#!forum/adaptive-programming
[feedback.py]: ../backend/monitoring/feedback.py
[Monitoring Notebook]: https://robomise.cz/media/exports/monitoring_latest.html
[monitoring_template.ipynb]: ../backend/monitoring/notebooks/monitoring_template.ipynb
[investigation_template.ipynb]: ../backend/monitoring/notebooks/investigation_template.ipynb
[Google Analytics]: https://analytics.google.com/analytics/web/#embed/report-home/a81667720w121094822p126691725/
[googleAnalytics.js]: ../frontend/src/sagas/googleAnalytics.js
[models.py]: ../backend/monitoring/models.py
[cronjobs.py]: ../backend/robomission/cronjobs.py
