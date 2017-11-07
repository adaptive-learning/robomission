# Static Assets

Most static files (JS, CSS, images)
are located in `//frontend/src`,
server under `/static/` URL prefix,
and accessed from ES6 modules via relative imports:

```
import greenBackgroundPath from '../images/background-green.png';
```

These files are handled completely automatically,
either by Webpack live server (`make liveserver`) during development,
or by Webpack + Django + Nginx on production
(orchestrated by `//deploy.sh` script,
which is called automatically after a push to server).

## Static Assets Pipeline

1. Webpack collects all assets, compiles ES6 modules,
and creates bundles to `//frontend/build/static`.
This step can be achieved locally by any of the following commands:

`make install` -> `make frontend` -> `npm run build`

2. Django is instructed to search for static files in this directory
(see `STATICFILES_DIRS` in `settings.py`).
Django's `collectstatic` command copies its content to
a directory specified by `STATIC_ROOT` in `settings.py`.

3. Nginx is instructed to serve all URLs starting with `/static/` prefix
in this  directory (see `location /static/` in `nginx.conf`).

The `deploy.sh` script calls
(1) `make install` to build frontend,
followed by (2) `collectstatic` to move static files
to the directory expected by Nginx.

If you need to access frontend app during backend development,
run `make install` to build frontend before running `make server`.
Django development server then accesses `//frontend/build/static`
for requests starting with `/static/` URL prefix
(which is specified by `STATIC_URL` in `settings.py`).


## Public Assets

Top-level public assets which needs to be accessed without `/static/` prefix
(such as `/favicon.ico` and `/robots.txt`)
resides in `//frontend/public` directory.
These files are not handled automatically
and each new top-level file requires change in the server configuration.

When frontend is built, these files are copied into `//frontend/build`.
Django then moves them further into backend static directory
under dedicated `public` namespace.
Each files requires a location record in `nginx.conf`
mapping URL (such as `/favicon.ico`)
to the respective location on server (`.../flocs/static/public/favicon.ico`)

For local testing, Django development server
can be instructed to serve these files by redirecting
their unprefixed URL (`/favicon.ico`)
to their prefixed form (`/static/public/favicon.ico`).
See `//backend/robomission/urls.py` for examples.
