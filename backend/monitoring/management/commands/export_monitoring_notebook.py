import logging
import re
import os
from django.conf import settings
from mmc.mixins import BaseCommand as MonitoredCommand
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import monitoring.data


logger = logging.getLogger(__name__)


def get_monitoring_notebook_template_path():
    path = os.path.join(
        settings.REPO_DIR, 'backend', 'monitoring', 'notebooks',
        'monitoring_template.ipynb')
    return path


def get_monitoring_notebook_output_path(datestamp):
    notebook_name = 'monitoring_{datestamp}.ipynb'.format(datestamp=datestamp)
    path = os.path.join(settings.EXPORTS_DIR, notebook_name)
    return path


def run_notebook(notebook):
    # See http://nbconvert.readthedocs.io/en/latest/execute_api.html
    ep = ExecutePreprocessor(timeout=120, kernel_name='django_extensions')
    # path = directory from where to execute the notebook
    path = os.path.join(settings.REPO_DIR, 'backend')
    ep.preprocess(notebook, {'metadata': {'path': path}})


def update_datestamp(notebook, new_datestamp):
    for cell in notebook['cells']:
        if cell['cell_type'] in {'code', 'markdown'}:
            cell['source'] = re.sub(r'\d{4}-\d{2}-\d{2}', new_datestamp, cell['source'])


class Command(MonitoredCommand):
    help = "Create a new monitoring notebook and put it into /media/exports'"

    def handle(self, *args, **options):
        logger.info('Management command called: export_monitoring_notebook')
        template_path = get_monitoring_notebook_template_path()
        logger.info('Using template: ' + template_path)
        with open(template_path) as infile:
            notebook = nbformat.read(infile, as_version=nbformat.NO_CONVERT)
        datestamp = monitoring.data.get_last_available_datestamp()
        update_datestamp(notebook, datestamp)
        run_notebook(notebook)
        output_path = get_monitoring_notebook_output_path(datestamp)
        with open(output_path, 'wt') as outfile:
            nbformat.write(notebook, outfile)
        logger.info('Done. New monitoring notebook stored at: ' + output_path)
