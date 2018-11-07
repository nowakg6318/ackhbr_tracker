'''
'''
import matplotlib.pyplot as plt

import HarborDataHandler as HDH

# Get Data DataFrame
file_path = '/Users/nowakg/Documents/Programs/Auckland Harbor Tracker/auckland_harbor_data.csv'
originaldf_columnname_list = (['Timestamp', 'Name', 'IMO', 'Type', 'Flag',
                               'Gross Tonnage', 'Deadweight Tonnage', 'Dock',
                               'Previous Port', 'Next Port'])

datadf_columnname_list = ['Name', 'IMO', 'Type', 'Flag', 'Gross Tonnage',
                          'Deadweight Tonnage', 'Dock', 'Previous Port',
                          'Next Port', 'Timestamp Enter', 'Timestamp Exit',
                          'Port Time']

seperation_columnname_name = 'Name'
data_df = HDH.Main(file_path, originaldf_columnname_list,
                   datadf_columnname_list, seperation_columnname_name)


# Port Time Histogram
def PlotPortTimeHistogram(data_df):
    data = data_df['Port Time'].astype('timedelta64[h]')
    bins = [4 * i + 0.1 for i in range(40)]
    plt.hist(data, bins, density=True)
    plt.xlabel('Hours in Port')
    plt.ylabel('Frequency')
    plt.title('Number of Hours Ships Spend in Auckland Ports')
    plt.show()


def PlotFlagHistogram(data_df):
    series = data_df['Flag'].value_counts()
    total = sum(series.values)
    plt.bar(series.index, series.values / total)
    plt.xticks(rotation=90)
    plt.ylabel('Frequency')
    plt.title('Flags Flown in Auckland Ports')
    plt.tight_layout()
    plt.show()


def PlotDeadWeightHistogram(data_df):
    series = (data_df.loc[data_df['Deadweight Tonnage'] > 0]
              ['Deadweight Tonnage'])

    bins = [2800 * i for i in range(25)]
    plt.hist(series, bins, density=True)
    plt.xlabel('Weight of Empty Ship (Tons)')
    plt.ylabel('Frequency')
    plt.title('Deadweight Tonnage Distribution in Auckland Ports')
    plt.show()


def PlotGrossTonnageHistogram(data_df):
    data = data_df['Gross Tonnage'].astype(int)
    plt.hist(data, bins=25, density=True)
    plt.xlabel('Carrying Capacity of Ship (Tons)')
    plt.ylabel('Frequency')
    plt.title('Gross Tonnage Distribution in Auckland Ports')
    plt.show()


def PlotShipTypeHistogram(data_df):
    series = data_df['Type'].value_counts()
    total = sum(series.values)
    plt.bar(series.index, series.values / total)
    plt.xticks(rotation=90)
    plt.ylabel('Frequency')
    plt.title('Type of Ships in Auckland Ports')
    plt.tight_layout()
    plt.show()


def PlotShipDockHistogram(data_df):
    series = data_df['Dock'].value_counts()
    total = sum(series.values)
    plt.bar(series.index, series.values / total)
    plt.xticks(rotation=90)
    plt.ylabel('Frequency')
    plt.title('Distribution of Ships using Docks')
    plt.tight_layout()
    plt.show()


def PlotPreviousPortHistogram(data_df):
    series = data_df['Previous Port'].value_counts()
    total = sum(series.values)
    plt.bar(series.index, series.values / total)
    plt.xticks(rotation=90)
    plt.ylabel('Frequency')
    plt.title('Distribution of Previous Ports')
    plt.tight_layout()
    plt.show()


def PlotDockSpecificTypeHistogram(data_df):
    dock_list = data_df['Dock'].unique().tolist()
    plot_list = [0] * len(dock_list)
    norm_const = len(data_df)
    for dock in dock_list:
        dock_df = data_df.loc[data_df['Dock'] == dock]
        series = dock_df['Type'].value_counts()
        plot_list[dock_list.index(dock)] = plt.bar(series.index,
                                                   series.values / norm_const)

    plt.xticks(rotation=90)
    plt.ylabel('Number of Ships')
    plt.title('Distribution of Ship Types in Auckland Ports.')
    plt.legend(tuple(plot_list), tuple(dock_list), title='Docks')
    plt.tight_layout()
    plt.show()


def PlotDockSpecificGrossTonnageHistogram(data_df):
    dock_list = data_df['Dock'].unique().tolist()
    plot_list = [0] * len(dock_list)
    for dock in dock_list:
        dock_df = data_df.loc[data_df['Dock'] == dock]
        series = dock_df['Gross Tonnage'].astype(int)
        plot_list[dock_list.index(dock)] = series

    plt.hist(plot_list, bins=50, stacked=True)
    plt.xticks(rotation=90)
    plt.ylabel('Number of Ships')
    plt.title('Distribution of Ship Types in Auckland Ports.')
    plt.tight_layout()
    plt.show()


def PlotTypeSpecificPortTime(data_df):
    dock_list = data_df['Type'].unique().tolist()
    plot_list = [0] * len(dock_list)
    for dock in dock_list:
        dock_df = data_df.loc[data_df['Type'] == dock]
        series = dock_df['Port Time'].astype('timedelta64[h]')
        plot_list[dock_list.index(dock)] = series

    plt.hist(plot_list, bins=50, stacked=True)
    plt.xticks(rotation=90)
    plt.ylabel('Number of Ships')
    #plt.title('Distribution of Ship Types in Auckland Ports.')
    plt.tight_layout()
    plt.show()


def PlotCorrelationDeadweightGrossTonnage(data_df):
    ship_type_list = data_df['Type'].unique().tolist()
    for ship_type in ship_type_list:
        ship_type_df = data_df.loc[data_df['Type'] == ship_type]
        deadweight_series = ship_type_df['Deadweight Tonnage']
        gross_series = ship_type_df['Gross Tonnage']
        plt.scatter(deadweight_series, gross_series,
                    c='C' + str(ship_type_list.index(ship_type)),
                    label=ship_type)
    plt.ylabel('Gross Tonnage (Tons)')
    plt.xlabel('Deadweight Tonnage (Tons)')
    plt.title('Deadweight Tonnage (tons) vs. Gross Tonnage (tons)')
    plt.legend(title='Ship Type', ncol=3)
    plt.show()


# Create Cool Histograms
PlotCorrelationDeadweightGrossTonnage(data_df)
PlotFlagHistogram(data_df)
PlotPortTimeHistogram(data_df)
PlotPreviousPortHistogram(data_df)
PlotDockSpecificTypeHistogram(data_df)
