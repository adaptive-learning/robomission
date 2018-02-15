"""Utils for working with domain.
"""
import json
import os
from django.conf import settings
from learn.serializers import DomainSerializer


def load_domain_from_file(name='domain/domain.json'):
    path = os.path.join(settings.REPO_DIR, 'backend', name)
    with open(path) as infile:
        data = json.load(infile)
    inject_tasks_data(data)
    serializer = DomainSerializer()
    domain = serializer.create_or_update(data)
    return domain


def inject_tasks_data(data):
    for task_data in data['tasks']:
        # TODO: unfake
        task_data['level'] = None  # TODO: remove level completely
        task_data['setting'] = '{}'  # TODO: use nested serializer
        task_data['solution'] = 'f'
