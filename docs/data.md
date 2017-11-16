# Data

To download a zip bundle with both static and collected data, access:

<https://robomise.cz/learn/export/latest/bundle>

To generate and download CSV tables from current data, use the export API at:

<https://robomise.cz/learn/export>

## Exporting Data

To export current data, run:
```
make export
```
This command generates CSV tables into directory `[media]/exports/robomission-[datestamp]/`.
In addition, it also creates a zip bundle `[media]/exports/robomission-[datestamp].zip`
and its copy `[media]/exports/robomission-latest.zip`,
which is downloadable through the latest-bundle link above.

To change exported attributes, edit serializers in:
```
//backend/learn/export.py
```

To add a new model to export, edit the list of registered entities in:
```
//backend/learn/management/commands/export_data.py
```
