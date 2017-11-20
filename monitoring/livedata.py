"""Fetching and caching current data from deployed system.
"""
from datetime import datetime
import json
import os
import urllib
import shutil

from django.conf import settings
import pandas as pd
import requests


# TODO: Unhardoce export-api URL (use robomission.settings)
def get_export_api_url():
    return 'https://robomise.cz/learn/export/'


def get_cache_dir(datestamp):
    dirname = 'robomission-' + datestamp
    path = os.path.join(settings.REPO_DIR, 'monitoring', '.data', datestamp, '')
    return path


def get_csv_path(dirpath, name):
    path = os.path.join(dirpath, name + '.csv')
    return path


def fetch_export_api():
    export_api_url = get_export_api_url()
    with urllib.request.urlopen(export_api_url) as response:
        api = json.load(response)
    return api


def fetch_and_store_csv(dirpath, name, url):
    path = get_csv_path(dirpath, name)
    print('Fetching', url, '...')
    with requests.get(url, stream=True) as response:
        with open(path, 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)
    print('Stored at:', path)


def fetch_and_store_current_data(dirpath):
    api = fetch_export_api()
    for key in api:
        if key.startswith('current/'):
            name = key[8:]
            url = api[key]
            fetch_and_store_csv(dirpath, name, url)


def fetch_current_data_if_not_cached(requested_datestamp, current_datestamp):
    cache_dir = get_cache_dir(requested_datestamp)
    if not os.path.isdir(cache_dir):
        if requested_datestamp != current_datestamp:
            raise NotImplementedError('Currently, only today data can be fetched.')
        os.makedirs(cache_dir, exist_ok=True)
        fetch_and_store_current_data(cache_dir)


def load_csv(dirpath, name):
    path = get_csv_path(dirpath, name)
    df = pd.read_csv(path, index_col='id')
    return df


def load_current_data_from_cache(datestamp):
    cache_dir = get_cache_dir(datestamp)
    data = {}
    for filename in os.listdir(cache_dir):
        name = filename.split('.')[0]
        data[name] = load_csv(cache_dir, name)
    return data


def get_current_data(datestamp=None):
    """Get data from the deployed system and storem them in cache.

    datestamp: When the data was created. String in 'Y-m-d' format.
        If None, current date is used.
        Currently, only data from current date can be fetched
        (but other can be still loaded from the local cache).
    """
    current_datestamp = datetime.now().strftime('%Y-%m-%d')
    datestamp = datestamp or current_datestamp
    fetch_current_data_if_not_cached(datestamp, current_datestamp)
    data = load_current_data_from_cache(datestamp)
    return data
