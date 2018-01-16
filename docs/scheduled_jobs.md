# Scheduled Jobs

The following jobs are currently executed periodically on the server:
* computing metrics (daily),
* exporting data (weekly),
* exporting monitoring notebook (weekly).

Cron jobs are defined in [cronjobs.py].

To apply changes, it's necessary to ssh to the server,
remove old jobs (`crontab -e` to edit)
and add new new jobs (`make schedule_jobs`).

You can check [table of executed management commands](<https://robomise.cz/admin/mmc/mmclog/>).
If a job fails, a mail is sent to the user who set the cron jobs
(which effectively means it is stored in some file on the server).
The results are also logged to `management.log`.

[cronjobs.py]: ../backend/robomission/cronjobs.py
