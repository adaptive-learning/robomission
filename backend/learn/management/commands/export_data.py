from datetime import datetime
import logging
from shutil import make_archive, copyfile
import os
from django.conf import settings
from mmc.mixins import BaseCommand as MonitoredCommand
from rest_framework.test import APIClient
import learn.export


logger = logging.getLogger(__name__)


class Command(MonitoredCommand):
    help = "Export all data for analysis into CSV files."

    entities_to_export = [
        ('tasks', learn.export.TaskViewSet),
        ('problemsets', learn.export.ProblemSetViewSet),
        ('task_sessions', learn.export.TaskSessionsViewSet),
        ('program_snapshots', learn.export.ProgramSnapshotsViewSet),
    ]

    def handle(self, *args, **options):
        logger.info('Management command called: export_data')
        datestamp = datetime.now().strftime('%Y-%m-%d')
        dirname = 'robomission-' + datestamp
        # The last empty path ('') is there to make it a directory, not a file.
        full_dirpath = os.path.join(settings.EXPORTS_DIR, dirname, '')
        self.stdout.write('Exporting entities to {path}'.format(path=full_dirpath))
        os.makedirs(full_dirpath, exist_ok=True)
        for entity_name, viewset_class in self.entities_to_export:
            self.export_entity(entity_name, viewset_class, full_dirpath)
        bundle_path = self.zip_bundle(full_dirpath)
        self.mark_zip_bundle_as_latest(bundle_path)

    def export_entity(self, entity_name, viewset_class, dirpath):
        file_name = entity_name + '.csv'
        file_path = os.path.join(dirpath, file_name)
        self.stdout.write(
            '-> exporting {entity} as {file_name}'
            .format(entity=entity_name, file_name=file_name))
        df = viewset_class().get_dataframe()
        df.to_csv(file_path)

    def zip_bundle(self, dirpath):
        # shutil.make_archive needs bundle output path without ".zip" as the
        # first argument.
        bundle_base = os.path.normpath(dirpath)
        root_dir = os.path.dirname(bundle_base)
        bundle_dirname = os.path.basename(bundle_base)
        path = make_archive(bundle_base, 'zip', root_dir=root_dir, base_dir=bundle_dirname)
        self.stdout.write('Created bundle to {path}'.format(path=path))
        return path

    def mark_zip_bundle_as_latest(self, bundle_path):
        latest_bundle_path = os.path.join(settings.EXPORTS_DIR, settings.EXPORT_BUNDLE_NAME)
        copyfile(bundle_path, latest_bundle_path)
        self.stdout.write('Copied as latest bundle to {path}'.format(path=latest_bundle_path))
