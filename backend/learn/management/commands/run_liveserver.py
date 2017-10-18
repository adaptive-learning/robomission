"""Command to run both Django development server and Webpack live server.
"""
import os
import subprocess
import atexit
import signal
from django.contrib.staticfiles.management.commands import runserver


class Command(runserver.Command):

    def inner_run(self, *args, **options):
        self.start_web()
        return super(Command, self).inner_run(*args, **options)

    def start_web(self):
        self.stdout.write('>>> Starting webpack')
        self.webpack_process = subprocess.Popen(
            ['cd frontend && npm run start'],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,)

        def kill_webpack_process(pid):
            self.stdout.write('>>> Closing webpack')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_webpack_process, self.webpack_process.pid)
