from datetime import datetime
from shutil import make_archive
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework.test import APIClient


class Command(BaseCommand):
    help = "Export all data for analysis into CSV files."

    entities_to_export = [
        'blocks',
        'toolboxes',
        'levels',
        'instructions',
        'tasks',
        'students',
        'task_sessions',
        'program_snapshots',
        'actions',
    ]

    def handle(self, *args, **options):
        datestamp = datetime.now().strftime('%Y-%m-%d')
        dirname = 'robomission-' + datestamp
        # The last empty path ('') is there to make it a directory, not a file.
        full_dirpath = os.path.join(settings.EXPORTS_DIR, dirname, '')
        self.stdout.write('Exporting entities to {path}'.format(path=full_dirpath))
        os.makedirs(full_dirpath, exist_ok=True)
        for entity_name in self.entities_to_export:
            self.export_entity(entity_name, full_dirpath)
        self.zip_bundle(full_dirpath)

    def export_entity(self, entity_name, dirpath):
        file_name = entity_name + '.csv'
        file_path = os.path.join(dirpath, file_name)
        self.stdout.write(
            '-> exporting {entity} as {file_name}'
            .format(entity=entity_name, file_name=file_name))
        # TODO: Create dataframes directly without url client, then use df.to_csv(path)
        client = APIClient()
        data = client.get('/learn/export/' + file_name).content.decode('utf-8')
        with open(file_path, 'w') as csvfile:
            csvfile.write(data)

    def zip_bundle(self, dirpath):
        # shutil.make_archive needs bundle output path without ".zip" as the
        # first argument.
        bundle_base = os.path.normpath(dirpath)
        root_dir = os.path.dirname(bundle_base)
        bundle_dirname = os.path.basename(bundle_base)
        path = make_archive(bundle_base, 'zip', root_dir=root_dir, base_dir=bundle_dirname)
        self.stdout.write('Created bundle to {path}'.format(path=path))
