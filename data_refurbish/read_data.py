import numpy as np
from pandas import Series, DataFrame
from json import load
from datetime import datetime


def acquire_dataframe(filename='../data/result.json'):
    data = read_data(filename)
    reduced_dict = reduce(data)
    df = DataFrame(reduced_dict)
    df = df.T
    df = set_dataframe_types(df)
    df['createdAt'] = df['createdAt'].map(convert_timestamp)
    df['updatedAt'] = df['updatedAt'].map(convert_timestamp)
    return df


def read_data(filename):
    with open(filename, 'r') as jsonFile:
        return load(jsonFile)


def reduce(json_data):
    series_dict = {}

    for key, value in json_data.items():
        if not value:
            continue
        new_value = {'nameWithOwner': value['nameWithOwner'],
                     'createdAt': value['createdAt'],
                     'updatedAt': value['updatedAt'],
                     'stars': value['stargazers']['totalCount'],
                     'releases': value['releases']['totalCount'],
                     'isFork': value['isFork'],
                     'forkCount': value['forkCount'],
                     'commitCount': value['defaultBranchRef']['target']['history']['totalCount'],
                     'description': value['description'],
                     'watchers': value['watchers']['totalCount'],
                     'diskUsage': value['diskUsage']}
        new_series = Series(new_value)
        series_dict[key] = new_series

    return series_dict


def set_dataframe_types(data_frame):
    data_types = {'nameWithOwner': str, 'createdAt': str, 'updatedAt': str, 'stars': np.int64,
                  'releases': np.int64, 'isFork': np.bool_, 'forkCount': np.int64, 'commitCount': np.int64,
                  'description': str, 'watchers': np.int64, 'diskUsage': np.int64}
    return data_frame.astype(data_types)


def convert_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
