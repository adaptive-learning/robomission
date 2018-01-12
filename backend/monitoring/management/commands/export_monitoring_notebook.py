import logging
import re
import os
from shutil import copyfile
from django.conf import settings
from mmc.mixins import BaseCommand as MonitoredCommand
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
import monitoring.data


logger = logging.getLogger(__name__)


def get_monitoring_notebook_template_path():
    path = os.path.join(
        settings.REPO_DIR, 'backend', 'monitoring', 'notebooks',
        'monitoring_template.ipynb')
    return path


def get_monitoring_notebook_output_path(datestamp, ext='ipynb'):
    notebook_name = 'monitoring_{datestamp}.{ext}'.format(
        datestamp=datestamp, ext=ext)
    path = os.path.join(settings.EXPORTS_DIR, notebook_name)
    return path


def update_datestamp(notebook, new_datestamp):
    for cell in notebook['cells']:
        if cell['cell_type'] in {'code', 'markdown'}:
            cell['source'] = re.sub(r'\d{4}-\d{2}-\d{2}', new_datestamp, cell['source'])


def run_notebook(notebook):
    # See http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # TODO: Specify 'django_extensions' kernel and make it work on the server.
    # The kernel can be set as follows:
    #   ep = ExecutePreprocessor(timeout=120, kernel_name='django_extensions')
    # This works locally, but on server, I wasn't able to create the kernel
    # (list available kernels by `jupyter kernelspec list`).
    # Default kernel currently works, given the `path` (directory from where to
    # execute the notebook) is set to //backend. It may fail if some Django
    # features are used in the notebook, but I haven't explored this.
    ep = ExecutePreprocessor(timeout=120)
    path = os.path.join(settings.REPO_DIR, 'backend')
    ep.preprocess(notebook, {'metadata': {'path': path}})


def export_notebook_to_html(notebook, datestamp, mark_as_latest=True):
    html_exporter = HTMLExporter()
    html, _resources = html_exporter.from_notebook_node(notebook)
    output_path = get_monitoring_notebook_output_path(datestamp, ext='html')
    with open(output_path, 'wt') as outfile:
        outfile.write(html)
    if mark_as_latest:
        latest_notebook_path = get_monitoring_notebook_output_path('latest', ext='html')
        copyfile(output_path, latest_notebook_path)


def save_notebook(notebook, datestamp):
    output_path = get_monitoring_notebook_output_path(datestamp)
    with open(output_path, 'wt') as outfile:
        nbformat.write(notebook, outfile)
    logger.info('New monitoring notebook stored at: ' + output_path)

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
        save_notebook(notebook, datestamp)
        export_notebook_to_html(notebook, datestamp, mark_as_latest=True)
