''' A module to parse the data collected by the Auckland Harbor Data Tracker.
'''

import pandas as pd

import pdb


class HarborDataHandler():
    '''
    '''

    def __init__(self, file_path):
        self.file_path = file_path
        self.original_df = self._CSVToDF()
        self.data_df = pd.DataFrame(columns=['Name', 'IMO',
                                             'Type', 'Flag', 'Gross Tonnage',
                                             'Deadweight Tonnage', 'Dock',
                                             'Previous Port', 'Next Port',
                                             'Timestamp Enter',
                                             'Timestamp Exit', 'Port Time'])

    def Handle(self) -> pd.DataFrame:
        '''
        '''

        for ship_name in self.original_df['Name'].unique():
            subset_df = self._CreateSubsetDF(ship_name)
            split_subsetdfs_list = self._SplitDFbyTimeIntervals(subset_df)
            equivalent_shipdf_series_list = self._CompressDFintoSeries(
                split_subsetdfs_list)

            self._AddSeriesListtoDataDF(equivalent_shipdf_series_list)

        return(self.data_df)

    def _CSVToDF(self):
        '''
        '''

        data_column_namelist = (['Timestamp', 'Name', 'IMO', 'Type', 'Flag',
                                 'Gross Tonnage', 'Deadweight Tonnage', 'Dock',
                                 'Previous Port', 'Next Port'])

        dataframe = pd.read_csv(self.file_path, names=data_column_namelist)
        dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])
        return(dataframe)

    def _CreateSubsetDF(self, ship_name: str) -> pd.DataFrame:
        '''
        '''

        subset_df = self.original_df.groupby(['Name']).get_group(ship_name)
        subset_df.sort_values(['Timestamp'])
        subset_df = subset_df.reset_index(drop=True)
        subset_df['Time Difference'] = subset_df['Timestamp'].diff(1)
        return(subset_df)

    def _SplitDFbyTimeIntervals(self, subset_df: pd.DataFrame):
        '''
        '''

        split_df_list = []
        index_split_list = (subset_df.loc[subset_df['Time Difference']
                            > pd.Timedelta('1 days')]
                            .index.tolist())

        index_split_list = [0] + index_split_list + [len(subset_df)]

        for i in range(len(index_split_list) - 1):
            split_df_list.append(
                subset_df[index_split_list[i]:index_split_list[i + 1]])

        return(split_df_list)

    def _CompressDFintoSeries(self, df_list: list) -> list:
        '''
        '''

        equivalent_series_list = []
        for df in df_list:
            df = df.reset_index(drop=True)
            time_enter = df['Timestamp'].loc[0]
            time_exit = df['Timestamp'].loc[len(df) - 1]
            port_time = time_exit - time_enter

            equivalent_series = (df[['Name', 'IMO',
                                     'Type', 'Flag', 'Gross Tonnage',
                                     'Deadweight Tonnage', 'Dock',
                                     'Previous Port', 'Next Port']]
                                 .loc[0].tolist()
                                 + [time_enter, time_exit, port_time])

            equivalent_series_list.append(equivalent_series)
        return(equivalent_series_list)

    def _AddSeriesListtoDataDF(self, series_list: list) -> None:
        '''
        '''

        for series in series_list:
            self.data_df.loc[len(self.data_df)] = series
