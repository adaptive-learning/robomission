# Monitoring

Even with careful testing,
there will always be some errors in the deployed system.
Monitoring tools help to spot these errors quickly
and provide as with a good guide on what we should improve
in next iterations to make our system great.

## Error Reports

Unhandled exceptions on the server: [adaptive-programming-errors google group](https://groups.google.com/forum/#!forum/adaptive-programming-errors).

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

(Sending user feedback is not currently implemented, but will be soon!)

Feedback from users: [adaptive-programming google group](https://groups.google.com/forum/#!forum/adaptive-programming)

## Collected Data Investigation

To explore collected data, follow instructions in [//docs/data.md](./data.md).
To generate current data to investigate an issue, run:
```
make monitoring
```
It will switch to the `monitoring` branch
and create a new jupyter notebook at `//monitoring/notebooks/analysis_datestamp.ipynb`
from [analysis_template.ipynb](../monitoring/notebooks/analysis_template.ipynb).

The key function here is `livedata.get_current_data()` which fetches
all current data from the deployed system, stores them in local cache (`//monitoring/.data/robomission-[datestamp]`) and returns a dictionary of dataframes with the data.

After the investigation, commit the new notebook,
but keep it in the `monitoring` branch
(don't merge these notebooks to the `master` branch).
Pushing your commit to the remote-tracking branch on GitHub
allows you to send a link to the investigation
(and GitHub generates previews of jupyter notebooks as we have seen for
[analysis_template.ipynb](../monitoring/notebooks/analysis_template.ipynb)).


## Google Analytics

* [Google Analytics - Romobission](https://analytics.google.com/analytics/web/#embed/report-home/a81667720w121094822p126691725/)
* [Google Analytics: Events Overview](https://analytics.google.com/analytics/web/#report/content-event-overview/a81667720w121094822p126691725/%3Foverview-dimensionSummary.selectedGroup%3Dvisitors%26overview-dimensionSummary.selectedDimension%3Danalytics.eventAction/)
* [//frontend/src/sagas/googleAnalytics.js](../frontend/src/sagas/googleAnalytics.js) - defines all messages sent to Google Analytics.
* You can set sending reports by mail (e.g. weekly).


## Admin Stats

TBA

## Logs

TBA
