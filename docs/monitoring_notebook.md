# Monitoring Notebook

* Performs basic analyses of collected data.
* Available at: <https://robomise.cz/media/exports/monitoring_latest.html>.
* Recomputed every week by cron.

## Extending analysis

* Edit [monitoring_template.ipynb] and verify that it works locally
  (`make export_monitoring_notebook`).
* Make sure the notebook specifies the `default` kernel. (If it limits you,
  we may try to make the `django_extensions` kernel work on the server.)
* Commit and push to the server (first staging, then production).
* Ssh to the server and verify the export manually by calling `make export_monitoring_notebook`.

## Implementation details

* We use cron to schedule exporting new data and monitoring notebook every week;
  see [cronjobs.md](./cronjobs.md) for details.
* The export of new data is described in [data.md](./docs.md).
* The export of the notebook is defined in [export_monitoring_notebook.py]:
  * The template is loaded and parsed using `nbformat` module.
  * The timestamp is replaced by the timestamp of the last exported data bundle.
  * The notebook is executed using `nbcovert` module.
  * The executed notebook is then exported to HTML using `nbconvert` module.
  * The rendered HTML file is saved in a public directory `/media/exports/monitoring_latest.html`.


## Future Plans
* Use Colab instead of Jupyter Notebook, since it would allow more easily to fork the monitoring notebok
  and perform additional ad-hoc analysis as needed (without any setup). Extending the template
  notebook would also be more comfortable (easier to verify that it works with the current data).
  
  
[monitoring_template.ipynb]: ../backend/monitoring/notebooks/monitoring_template.ipynb
[export_monitoring_notebook.py]: ../backend/monitoring/management/commands/export_monitoring_notebook.py
