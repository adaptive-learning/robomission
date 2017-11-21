# Deployment

Deployment process has 3 steps:
* local development,
* staging,
* production.


## Adaptive Learning Server

To access the Adaptive Learning server and publish new versions:
1. Ask an admin to create an account on the server for you.
   He will also need to add your public ssh key to a list of known public keys.

2. Add the production and staging remotes to your local repository:

        git remote add staging git@al.thran.cz:flocs-staging.git
        git remote add production git@al.thran.cz:flocs.git


## Staging

Purpose: test the new version in the setting which is as close as possible to the production environment.


To publish a new version to the staging, run:
```
git push staging
```

Use the staging version running at https://staging.robomise.cz
to test that everything works as expected.


## Production

To publish the new version to the production, run:
```
git push production
```

The public URL is https://robomise.cz.
<!-- (...) for Czech localization and https://en.robomise.cz/ for English localization. -->


## Related Links
* [//deploy.sh](../deploy.sh) - commands that are run on the server after each push.
* [//docs/static-assets.md](./static-assets.md) - static files handling.
