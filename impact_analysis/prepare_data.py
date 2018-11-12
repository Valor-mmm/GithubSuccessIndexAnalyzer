from json import load
from pandas import Series
from datetime import datetime
from re import compile, RegexFlag, sub

from data_refurbish.read_data import acquire_dataframe

is_initial_commit_pattern = compile(r'^initial commit\.?\n?$', flags=RegexFlag.IGNORECASE)
replaceForDisplay = compile(r'\W', flags=RegexFlag.MULTILINE)
replaceForDisplayDigits = compile('^\d+', flags=RegexFlag.MULTILINE)


def prepare_data(repo_data_file, commit_data_file):
    df = acquire_dataframe(repo_data_file)
    del df['description']
    df = filter_forks(df)
    df['initialCommitMsg'] = get_commit_message_series(commit_data_file, df)
    df = remove_any_nan(df)
    apply_map(success_formula, 'successIndex', df)
    apply_map(is_conform, 'isConform', df)
    return df


def filter_forks(dataframe):
    df_total: int = len(dataframe.index)
    df = dataframe[~ dataframe['isFork']]
    df_no_fork: int = len(df.index)
    print('Removed ' + str(df_total - df_no_fork) + ' fork repositories.')
    print('Dataframe is now of size: ' + str(df_no_fork))
    return df


def get_commit_message_series(commit_data_file, df):
    data = read_commit_message_data(commit_data_file)
    commit_dict = {}

    # names = list(df.index)
    # counter = 0

    for entry in data:
        repo_descriptor = entry['repoName'].partition('/')
        owner = sub(replaceForDisplay, '', repo_descriptor[0])
        owner = sub(replaceForDisplayDigits, '', owner)
        name = sub(replaceForDisplay, '', repo_descriptor[2])
        commit_dict[owner + '_' + name] = entry['message']
        # if not (owner + '_' + name) in names:
        #    counter += 1
    # print(str(counter) + ' commit messages could not be set.')
    return Series(commit_dict)


def read_commit_message_data(commit_data_file):
    with open(commit_data_file) as f:
        return load(f)


def success_formula(series):
    active_timedelta = series.updatedAt - series.createdAt
    commit_value = series.commitCount / 8
    positive = series.stars + series.forkCount + series.watchers + active_timedelta.days + commit_value
    timedelta = datetime.now() - series.updatedAt
    value = positive / (timedelta.days + 1)
    return value


def apply_map(formula, name, dataframe):
    new_row = {}
    for index, row in dataframe.iterrows():
        new_row[index] = formula(row)

    dataframe[name] = Series(new_row)


def remove_any_nan(df):
    print('NaN values in the following columns:\n' + str(df.isna().any()))
    df_size = len(df.index)
    full_df = df.dropna(how='any', axis=0)
    full_df_size = len(full_df.index)
    print('Removed ' + str(df_size - full_df_size) + ' NAN repositories.')
    print('Dataframe is now of size: ' + str(full_df_size))
    return full_df


def is_conform(series):
    if is_initial_commit_pattern.match(series.initialCommitMsg):
        return True
    return False
