"""Utils for reusingJS code.
"""
from functools import singledispatch
import json
import os
import re
from subprocess import Popen, PIPE
from django.conf import settings


def run_script(script_name, input_text):
    # TODO: better error handling
    path = os.path.join(settings.JS_TOOLS_DIR, script_name)
    with Popen([settings.JS_NODE_PATH, path], stdout=PIPE, stdin=PIPE, stderr=PIPE) as js_process:
        enc_stdout, enc_stderr = js_process.communicate(input=input_text.encode())
    stdout = enc_stdout.decode()
    stderr = enc_stderr.decode()
    if stderr:
        raise ValueError('Running JS script {name} failed.\n{description}'.format(
            name=script_name, description=create_description(input_text, stdout, stderr)))
    #result = camel_to_snake_case(json.loads(stdout))
    result = json.loads(stdout)
    return result


def create_description(input_text, stdout, stderr):
    description = '\n'.join([
        '##### input: #####', input_text,
        '##### output: #####', stdout,
        '##### error: #####', stderr,
        '##########'
    ])
    return description


@singledispatch
def camel_to_snake_case(name):
    partially_underscored = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    fully_underscored = re.sub('([a-z0-9])([A-Z])', r'\1_\2', partially_underscored)
    return fully_underscored.lower()


@camel_to_snake_case.register(dict)
def _camel_to_snake_case(mapping):
    return {camel_to_snake_case(key): value for key, value in mapping.items()}
