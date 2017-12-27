# Deployment

Deployment process has 3 steps:
* local development,
* staging,
* production.


## Access to the Server

To access the Adaptive Learning server and publish new versions:

1. Ask an admin to create an account on the server for you.
   (The account is not necessary to push new versions to the server,
    but sometimes you will need to ssh to the server
    to view logs and solve on-server issues.)

2. Generate a [ssh key pair](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/).
  Give your public key to the admin and he will add it to the list of authorized keys
  (`/var/git/.ssh/authorized_keys`).

2. Add the production and staging remotes to your local repository:

        git remote add staging git@al.thran.cz:flocs-staging.git
        git remote add production git@al.thran.cz:flocs.git


## Staging

Purpose: test the new version in the setting which is as close as possible to the production environment.

To publish a new version to the staging, run:
```
git push staging
```

Use the staging version running at <https://staging.robomise.cz>
to test that everything works as expected.


## Production

To publish the new version to the production, run:
```
git push production
```

The public URL is <https://robomise.cz> for Czech version
and <https://en.robomise.cz> for English version.


## Setting Up New Server

First, set up nginx, gunicorn, git and PostgreSQL,
similarly [as on the AL server](<https://github.com/adaptive-learning/project-deployment>).
After first `git push`, there are some additional manual steps:

* `python backend/manage.py createsuperuser`
* `make socialapps` (required for login via social apps)
* `make schedule_jobs` (uses cron to schedule periodic jobs)


## Related Links
* [//deploy.sh](../deploy.sh) - commands that are run on the server after each push.
* [//docs/static-assets.md](./static-assets.md) - static files handling.
