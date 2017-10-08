from django.core.management.base import BaseCommand
#from learn.models import Block, Toolbox, Level, Task, Instruction


class Command(BaseCommand):
    help = "Loads static data into the database."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Data are loaded in migrations, use "make migrate".'))
