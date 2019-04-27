# Scheduled Jobs

The following jobs are currently executed periodically on the server:
* computing metrics (daily),
* exporting data (weekly),
* exporting monitoring notebook (weekly).

Cron jobs are defined in [cronjobs.py].

To apply changes, it's necessary to ssh to the server,
remove old jobs (`crontab -e` to edit)
and add new jobs (`make schedule_jobs`).

You can check [table of executed management commands](<https://robomise.cz/admin/mmc/mmclog/>).
If a job fails, a mail is sent to the user who set the cron jobs
(which effectively means it is stored in some file on the server).
The results are also logged to `management.log`.

[cronjobs.py]: ../backend/robomission/cronjobs.py


## Implementation Details

The jobs are scheduled and run by `cron` according to the `crontab` file
which is updated programatically when `make schedule_jobs` is called.
The `make schedule_jobs` command uses [django-crontab](https://pypi.org/project/django-crontab/)
extension to edit the crontab file. The extenstion slightly simplifies creating correct crontab entries
which activate virtual environment and call a specified django management command.
