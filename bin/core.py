from datetime import datetime

import pandas as pd
import os
import sys

from bin.config import INPUT_FILES, OUT_COLUMNS, PORT_NAME, SUMMARY_OPTIONS
from bin.pdf_generator import generate_pdf_file
from bin.charts import bar_of_pie_protocols_chart, dest_ports_chart, get_summary_chart
from bin.charts import bytes_per_L4_protocol_chart

folder_with_csv_files = '../resources/' + INPUT_FILES


def get_data(files_count=3, get_ports=10):
    """
    :param files_count: number of files to import from netflow_csv folder, default is 3
	:return: dictionary
	"""
    with os.scandir(folder_with_csv_files) as entries:
        raw_data = dict()
        protocols = dict()
        ports = dict()
        for entry in entries:
            try:
                if len(raw_data) < files_count:
                    print('processing file {}'.format(entry.name))
                    print(len(raw_data))
                    df = pd.read_csv(folder_with_csv_files + '/' + entry.name
                                     , low_memory=False
                                     , usecols=['ts', 'te', 'td', 'sa', 'da', 'sp', 'dp', 'pr', 'ibyt']
                                     , index_col=None
                                     , sep=',')
                    series_summary = df.iloc[-1, :6]
                    dict_summary = dict(series_summary)
                    file_name = str(entry.name)
                    date = str(entry.name).split('.')[1]
                    # get bytes per protocols dictionary
                    protocols_df = df.groupby(['pr'], as_index=False)['ibyt'].sum()
                    protocols_df.set_index('pr', inplace=True)
                    protocols = protocols_df.to_dict('index')
                    # ports
                    df = df[~df.dp.isin(['0', '21548'])]
                    df = df.loc[df.dp < 49152]
                    ports_df = df.groupby(['dp'], as_index=False)['sa'].count().sort_values(by='sa', ascending=False)[:get_ports]
                    temp_list = ports_df.to_dict(orient='records')
                    for item in temp_list:
                        new_key = list(item.values())[0]
                        new_value = list(item.values())[1]
                        ports[new_key] = new_value
                    raw_data[file_name] = [dict_summary, date, protocols, ports]
            except FileNotFoundError:
                print('get_Data(): check path to file or file name')
                sys.exit()
    return raw_data


def bytes_per_protocols(df, transport_protocols=False):
    """
	:param df: input dataframe
	:param transport_protocols: when True only TCP and UDP protocols taken into consideration
	:return: dictionary with protocol name as a key and number of bytes as a value
	"""
    protocols = {}
    if transport_protocols:
        df = df[df.pr.isin(['TCP', 'UDP'])]
        protocols = df.groupby(['pr'], as_index=False)['ibyt'].sum()
    else:
        try:
            new_df = df.groupby(['pr'], as_index=False)['ibyt'].sum()
        except KeyError:
            print(f'missing column in input dataframe')
        temp_list = new_df.to_dict(orient='records')
        for item_dict in temp_list:
            new_key = list(item_dict.values())[0]
            new_value = list(item_dict.values())[1]
            protocols[new_key] = new_value
    return protocols


def dest_ports(df, get_ports=10):
    """
	:param df: input dataframe
	:param get_results: number of analyzed ports (in descending order in terms of connections number)
	:return: dictionary with port number and number of connections
	"""
    ports = {}
    try:
        df = df[~df.dp.isin(['0', '21548'])]
        df = df.loc[df.dp < 49152]
        new_df = df.groupby(['dp'], as_index=False)['sa'].count().sort_values(by='sa', ascending=False)[:get_ports]
    except KeyError:
        print(f'missing column in input dataframe')
    temp_list = new_df.to_dict(orient='records')
    for item in temp_list:
        new_key = list(item.values())[0]
        new_value = list(item.values())[1]
        ports[new_key] = new_value
    print(ports)
    return ports


def get_summary(files_count=1):
    """
	function takes only the last row from each CSV file, which is the summary of the 5 minutes measure cycle
	:param files_count: number of files to import
	:return: data frame with following columns:
	- date - column of type datetime
	- flows
	- bytes
	- packets
	- average bites per seconds
	- average packets per seconds
	- average bytes per packet
	"""
    dfs = []
    out = pd.DataFrame()
    with os.scandir(folder_with_csv_files) as entries:
        for entry in entries:
            try:
                if len(dfs) < files_count:
                    df = pd.read_csv(folder_with_csv_files + '/' + entry.name,
                                     usecols=['ts', 'te', 'td', 'sa', 'da', 'sp'], index_col=None, sep=',',
                                     low_memory=False).tail(1)
                    df.rename(columns={'ts': 'flows',
                                       'te': 'bytes',
                                       'td': 'packets',
                                       'sa': 'avg_bps',
                                       'da': 'avg_pps',
                                       'sp': 'avg_bpp'},
                              inplace=True)
                    df['date'] = str(entry.name).split('.')[1]
                    dfs.append(df)
                    print(len(dfs))
            except FileNotFoundError:
                print('get_summary(): check path to file or file name')
    out = pd.concat(dfs, axis=0, ignore_index=True)
    out['date'] = out['date'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H%M'))
    return out


if __name__ == '__main__':
    input_data = get_data(files_count=1)
    print(input_data)
    # for i in input_data.items():
    #     for j in i[1][0].items():
    #         print(j)
    # df = input_data[0]
    # dest_ports_chart(dest_ports(df))
    # bpp = bytes_per_protocols(df, transport_protocols=True)
    # bytes_per_L4_protocol_chart(bpp)
    # bpp_all = bytes_per_protocols(df)
    # bar_of_pie_protocols_chart(bpp_all)
    # for sum in SUMMARY_OPTIONS:
    #     get_summary_chart(get_summary(1), option=sum)
    # generate_pdf_file(input_data[1])
