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
| [Dashboard]        | [MonitoringPage.jsx] | |
| [DB Admin]         | [admin.py] | |
| [Metrics]          | [metrics.py] | management.log |
| [Errors]           | [settings.py]<sup>\*</sup> | robomission.log |
| [Feedback]         | [feedback.py] | feedback.log |
| [Google Analytics] | [googleAnalytics.js] | |

<sup>\*</sup> Related options in `settings.py` are ADMIN and LOGGING.

## Metrics

* All metrics are stored in a single DB table ([monitoring.models.Metric][models.py]).
* They are defined in [metrics.py].
* Recent metrics are visualized in [the monitoring dashboard][Dashboard].
* Metrics recomputed every night using cron.
  Cron jobs are defined in [cronjobs.py].
  To apply changes, it's necessary to ssh to the server,
  remove old jobs (`crontab -e` to edit)
  and add new new jobs (`make schedule_jobs`).
* You can check [table of executed management commands](<https://robomise.cz/admin/mmc/mmclog/>).
  If a job fails, a mail is sent to the user who set the cron jobs
  (which effectively means it is stored in some file on the server).
  The results are also logged to `management.log`.

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

To explore collected data, follow instructions in [//docs/data.md](./data.md).
All collected data are exported once a week.
If it's not enough and you need to generate current data to investigate an issue, run:
```
make monitoring
```
It will switch you to the `monitoring` branch
and create a new jupyter notebook at `//backend/monitoring/notebooks/analysis_datestamp.ipynb`
from [analysis_template.ipynb](../backend/monitoring/notebooks/analysis_template.ipynb).

The key function here is `livedata.get_current_data()` which fetches
all current data from the deployed system, stores them in local cache (`//backend/monitoring/.data/robomission-[datestamp]`) and returns a dictionary of dataframes with the data.

After the investigation, commit the new notebook,
but keep it in the `monitoring` branch
(don't merge these notebooks to the `master` branch).
Pushing your commit to the remote-tracking branch on GitHub
allows you to send a link to the investigation
(and GitHub generates previews of jupyter notebooks as we have seen for
[analysis_template.ipynb](../backend/monitoring/notebooks/analysis_template.ipynb)).


## Google Analytics

* [Google Analytics - Romobission](https://analytics.google.com/analytics/web/#embed/report-home/a81667720w121094822p126691725/)
* [googleAnalytics.js] - defines all messages sent to Google Analytics.
* You can set sending reports by mail (e.g. weekly).


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
[Google Analytics]: https://analytics.google.com/analytics/web/#embed/report-home/a81667720w121094822p126691725/
[googleAnalytics.js]: ../frontend/src/sagas/googleAnalytics.js
[models.py]: ../backend/monitoring/models.py
[cronjobs.py]: ../backend/robomission/cronjobs.py
