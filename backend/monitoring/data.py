"""Fetching and caching production data.
"""
from datetime import datetime
import io
import os
from zipfile import ZipFile

from django.conf import settings
import pandas as pd
import requests


# TODO: Unhardcode this URL (use robomission.settings)
def get_latest_bundle_url():
    return 'https://robomise.cz/media/exports/robomission-latest.zip'


def get_cache_dir(datestamp=None):
    path = os.path.join(settings.REPO_DIR, 'backend', 'monitoring', '.data')
    os.makedirs(path, exist_ok=True)
    if datestamp:
        path = os.path.join(path, 'robomission-' + datestamp)
    dirpath = os.path.join(path, '')
    return dirpath


def get_csv_path(dirpath, name):
    path = os.path.join(dirpath, name + '.csv')
    return path


def get_available_datestamps():
    cache_dir = get_cache_dir()
    bundle_names = os.listdir(cache_dir)  # they include "robomission-" prefix
    datestamps = [name.split('-', 1)[1] for name in bundle_names]
    return datestamps


def load_csv(dirpath, name):
    path = get_csv_path(dirpath, name)
    df = pd.read_csv(path, index_col='id')
    return df


def load_data_from_cache(datestamp):
    cache_dir = get_cache_dir(datestamp)
    data = {}
    for filename in os.listdir(cache_dir):
        name = filename.split('.')[0]
        data[name] = load_csv(cache_dir, name)
    print('Data loaded from cache ({cache}).'.format(cache=cache_dir))
    return data


def fetch_latest_bundle():
    url = get_latest_bundle_url()
    dirpath = get_cache_dir()
    print('Fetching', url, '...')
    # TODO: Rewrite to first download, then unzip, (then remove zip file) to
    # limit future problems with data not fitting into memory.
    with requests.get(url, stream=True) as response:
        zipdir = ZipFile(io.BytesIO(response.raw.read()))
        zipdir.extractall(path=dirpath)
    print('Stored at:', dirpath)


def check_fetching_possible(datestamp_wanted, fetch_wanted):
    """Raise ValueError if fetching is not possible.
    """
    current_datestamp = datetime.now().strftime('%Y-%m-%d')
    available_datestamps = get_available_datestamps()
    if available_datestamps:
        last_available_datestamp = max(available_datestamps)
        if datestamp_wanted < last_available_datestamp:
            raise ValueError(
                "Choose one of the chached bundles ({cached}) "
                "or current datestamp ({current})."
                .format(
                    cached=', '.join(available_datestamps) or 'none available',
                    current=current_datestamp))
    if not fetch_wanted:
        raise ValueError(
            "Choose one of the chached bundles ({cached}) "
            "or allow fetching by setting fetch=True."
            .format(
                cached=', '.join(available_datestamps) or 'none available'))


def fetch_latest_bundle_if_possible(datestamp_wanted, fetch_wanted):
    check_fetching_possible(datestamp_wanted, fetch_wanted)
    fetch_latest_bundle()


def get_production_data(datestamp, fetch=True):
    """Get data from the production system and store them in cache.

    Args:
        datestamp:
            When the data was created. String in 'Y-m-d' format.
            Data will be loaded from local cache, using the first export from
            date >= given datestemp.
        fetch:
            If there are no cached data after given datestamp,
            it will fetch the latest export from the server.

    Return:
        dict mapping names of entities to the DataFrames
    """
    available_datestamps = get_available_datestamps()
    if datestamp not in available_datestamps:
        fetch_latest_bundle_if_possible(datestamp, fetch)
        new_datestamp = max(get_available_datestamps())
        if new_datestamp != datestamp:
            raise ValueError('Change datestamp to: ' + new_datestamp)
    data = load_data_from_cache(datestamp)
    return data
