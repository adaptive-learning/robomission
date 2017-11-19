"""Fetching and caching current data from deployed system.
"""
import urllib, json
import pandas as pd


# TODO: Unhardoced export-api URL (use robomission.settings)
def get_export_api_url():
    return 'https://robomise.cz/learn/export/'


def fetch_export_api():
    export_api_url = get_export_api_url()
    with urllib.request.urlopen(export_api_url) as response:
        api = json.load(response)
    return api


def fetch_dataframe(url):
    print('Fetching', url)
    with urllib.request.urlopen(url) as response:
        df = pd.read_csv(response, index_col='id')
    return df


# TODO: Caching - store downloaded data in .data and onnly download new if
# not already downloaded today.
def get_current_data():
    api = fetch_export_api()
    data = {}
    for key in api:
        if key.startswith('current/'):
            name = key[8:]
            df = fetch_dataframe(api[key])
            data[name] = df
    return data
