# Localization

## How Is the Language Determined

Language of the app is determined purely from URL
(Czech: <https://robomise.cz>, English: <https://en.robomise.cz>).
Neither cookies, nor session state, nor browser setting are used.
The URL approach is the most explicit and is friendly to search engines.

Language of the backend API is determined by the [LocaleMiddleware][1]
using "Accept-Language" header in sent request.
The header is set in [//frontend/src/config.js](../frontend/src/config.js)
based on the URL.
Default language is set to "cs" (`settings.LANGUAGE_CODE`).
See [DRF:internationalization][2] for details.

  [1]: https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#how-django-discovers-language-preference
  [2]: http://www.django-rest-framework.org/topics/internationalization/

## Where Do Localized Messages Live

We attempt to put all messages in a single directory on frontend,
including task names, instrustions, and Blockly blocks.

* Czech: [//frontend/src/localization/messages-cs.js](../frontend/src/localization/messages-cs.js)
* English: [//frontend/src/localization/messages-en.js](../frontend/src/localization/messages-en.js)

Backend only operates with message labels,
which are turned into the localized messages later on the frontend.
For instance, instructions have names such as "block.repeat" or "block.while",
and localization files have keys for each of them
("instruction.block.repeat", "instruction.block.while").
This strategy makes the localization simple
and avoids needs for
[setting translation on backend](https://docs.djangoproject.com/en/1.8/topics/i18n/translation/)
and [multilingual models](http://django-modeltranslation.readthedocs.org/).

The only current exception to the "single place for localization" rule
are messages sent by DRF;
for example, when an invalid email address is sent in a form.
(But we will move it to the frontend as well,
if we will want to customize the messages in the future.)

## How to Use Localization

If possible, use `Text` component and set `id` to the message ID:

```
import { Text } from '../localization';
...
<Text id="Tasks" />
```

If you can't use component, use `translate` function:

```
import { translate } from '../localization';
...
translate('blockly.start')
```

Functions and components for localization are defined in
[//frontend/src/localization/](../frontend/src/localization/.js).
Under the hood, they use [react-intl](https://github.com/yahoo/react-intl) library,
so refer there for advanced features, such as pluralization or interpolation.

## How to Test Localization

You can access
Czech localization at <http://localhost:8000/>
and English localization at <http://en.localhost:8000/>.
For a liveserver, there is one additional step required
to allow for different host:
copy [//frontend/.env.development](../frontend/.env.development)
into `//frontend/.env.development.local` and set `HOST=en.localhost`.
