# Data

Zip bundle with both static and collected data:

<https://robomise.cz/learn/export/latest/bundle>

Complete export API,
which allows to generate and download CSV tables from the current data:

<https://robomise.cz/learn/export>

Data description (as a jupyter notebook):

<https://github.com/adaptive-learning/robomission/blob/master/docs/data.ipynb>

## Exporting Data

* Data are exported once a week, as scheduled in
  [cronjobs.py](../backend/robomission/cronjobs.py).
  (See [cronjobs.md](./cronjobs.md) for details.)

* To export current data manually, run `make export`.
  This command generates CSV tables into directory `[media]/exports/robomission-[datestamp]/`.
  In addition, it also creates a zip bundle `[media]/exports/robomission-[datestamp].zip`
  and its copy `[media]/exports/robomission-latest.zip`,
  which is downloadable through the latest-bundle link above.

* To change exported attributes, edit serializers in [export.py](../backend/learn/export.py).

* To add a new model to export, edit the list of registered entities in
  [export_data.py](../backend/learn/management/commands/export_data.py).
