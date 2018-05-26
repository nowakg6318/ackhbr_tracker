''' A module to parse the data collected by the Auckland Harbor Data Tracker.
'''

import pandas as pd
import numpy as np

import pdb


def Main(file_path, datadf_columns=['Name', 'IMO', 'Type', 'Flag',
                                    'Gross Tonnage', 'Deadweight Tonnage',
                                    'Dock', 'Previous Port', 'Next Port',
                                    'Timestamp Enter', 'Timestamp Exit',
                                    'Port Time']):
    '''
    '''

    original_df = _CSVtoDF(file_path)
    data_df = _CreateDataDF(datadf_columns)
    for ship_df in _SplitDFbyUniqueRowValue(original_df, 'Name'):
        ship_trip_df_list = _SplitDFbyTimeIntervals(ship_df)
        ship_trips_df = _CompressDFListintoDF(ship_trip_df_list,
                                              datadf_columns)
        data_df = _AppendDFtoDataDF(data_df, ship_trips_df)
    return(data_df)


def _CSVtoDF(file_path: str) -> pd.DataFrame: # noqa 
    '''
    '''

    data_column_namelist = (['Timestamp', 'Name', 'IMO', 'Type', 'Flag',
                             'Gross Tonnage', 'Deadweight Tonnage', 'Dock',
                             'Previous Port', 'Next Port'])

    dataframe = pd.read_csv(file_path, names=data_column_namelist)
    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])
    return(dataframe)


def _CreateDataDF(column_name_list: list) -> pd.DataFrame:
    return(pd.DataFrame(columns=column_name_list))


def _SplitDFbyUniqueRowValue(original_df, column_name) -> list:
    '''
    '''

    df_list = []
    groupby_object = original_df.groupby(column_name)
    print(len(groupby_object.groups))
    for ship_name in groupby_object.groups.keys():
        df = groupby_object.get_group(ship_name)
        df.sort_values(['Timestamp'])
        df = df.reset_index(drop=True)
        df['Time Difference'] = df['Timestamp'].diff(1)
        df_list.append(df)
    return(df_list)


def _SplitDFbyTimeIntervals(df: pd.DataFrame):
    '''
    '''

    split_df_list = []
    index_split_list = (df.loc[df['Time Difference']
                        > pd.Timedelta('1 days')]
                        .index.tolist())

    index_split_list = [0] + index_split_list + [len(df)]

    for i in range(len(index_split_list) - 1):
        split_df_list.append(
            df[index_split_list[i]:index_split_list[i + 1]])

    return(split_df_list)


def _CompressDFListintoDF(df_list: list,
                          column_name_list: list) -> pd.DataFrame:
    '''
    '''

    new_df = pd.DataFrame(columns=column_name_list)
    for df in df_list:
        df = df.reset_index(drop=True)
        nontime_df_data_list = (df[['Name', 'IMO', 'Type', 'Flag',
                                    'Gross Tonnage', 'Deadweight Tonnage',
                                    'Dock', 'Previous Port', 'Next Port']]
                                .loc[0].tolist())

        time_enter = df['Timestamp'].loc[0]
        time_exit = df['Timestamp'].loc[len(df) - 1]
        port_time = time_exit - time_enter
        new_df.loc[len(new_df)] = (nontime_df_data_list
                                   + [time_enter, time_exit, port_time])

    return(new_df)


def _AppendDFtoDataDF(data_df: pd.DataFrame, small_df: pd.DataFrame) -> None:
    '''
    '''

    data_df = data_df.append(small_df)
    data_df = data_df.reset_index(drop=True)
    return(data_df)
