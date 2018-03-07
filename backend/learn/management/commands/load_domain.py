from django.core.management.base import BaseCommand
from django.conf import settings
from learn.domain_parser import load_domain_from_file


class Command(BaseCommand):
    help = 'Load domain data and stores them to DB.'

    def handle(self, *args, **options):
        self.stdout.write('Loading domain...')
        path = 'domain/domain.json'
        domain = load_domain_from_file(path)
        self.stdout.write(self.style.SUCCESS(
            ('Domain "{domain}" loaded: '
             '{m} missions, {c} chunks, {t} tasks, {x} toolboxes, {b} blocks.'
            ).format(
                domain=domain.name,
                m=domain.missions.count(),
                c=domain.chunks.count(),
                t=domain.tasks.count(),
                x=domain.toolboxes.count(),
                b=domain.blocks.count())))
