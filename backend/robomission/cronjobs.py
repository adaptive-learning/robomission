"""Settings for periodics jobs which should be scheduled using cron.
"""

EVERYDAY_4AM = '* 4 * * *'
SATURDAY_3AM = '* 3 * * 6'


def cronjob(schedule, cmd, logfile):
    """Return 5-tuple describing a single cronjob.

    The format of the result is as expected by django-crontab:
    (schedule, command, positional arguments, optional arguments, command suffix)
    """
    log_output = '>> {logfile} 2>&1'.format(logfile=logfile)
    return (schedule, 'django.core.management.call_command', [cmd], {}, log_output)


def get_cronjobs(logfile):
    """Create a list of cronjob descriptions.

    Each job is described by a 5-tuple as expected by the django-crontab library.
    Use this function in settings.py to set CRONJOBS option:
    ```
    CRONJOBS = get_cronjobs(logfile='path-to-log-file')
    ```
    """
    cronjobs_list = [
        cronjob(EVERYDAY_4AM, 'compute_metrics', logfile),
        cronjob(SATURDAY_3AM, 'export_data', logfile)]
    return cronjobs_list


def get_crontab_command_prefix(on_staging=False, on_production=False):
    """Return command that sets environment variables for cron.

    Use this function in settings.py to set CRONTAB_COMMAND_PREFIX option.
    """
    assert not on_staging or not on_production
    if on_staging:
        return 'source /usr/local/share/.virtualenvs/flocs-staging/bin/postactivate &&'
    if on_production:
        return 'source /usr/local/share/.virtualenvs/flocs/bin/postactivate &&'
    return ''
