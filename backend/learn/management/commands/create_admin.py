from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create superuser 'admin' with password 'robomise'."

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            dest='password',
            default='robomise',
        )

    def handle(self, *args, **options):
        password = options['password']
        if User.objects.filter(username='admin').exists():
            admin = User.objects.get(username='admin')
            admin.set_password(password)
            admin.save()
            self.stdout.write('User "admin" already exists.')
            self.stdout.write(
                'Set password to "{password}".'
                .format(password=password))
        else:
            User.objects.create_superuser('admin', '', password)
            self.stdout.write(
                'Created superuser "admin" with password "{password}".'
                .format(password=password))
