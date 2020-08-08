import math

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime as dt
from bin.config import INPUT_FILES, PORT_NAME, SUMMARY_OPTIONS, NUMBER_OF_PORTS
from bin.pdf_generator import generate_pdf_file
from bin.charts import destination_ports_chart, get_summary_chart
from bin.charts import bytes_per_L4_protocol_chart

folder_with_csv_files = '../resources/' + INPUT_FILES


def get_data(files_count=3):
    """
    :param files_count: number of files to import from netflow_csv folder, default is 3
	:return: dictionary
	"""
    with os.scandir(folder_with_csv_files) as entries:
        raw_data = dict()
        for entry in entries:
            try:
                if len(raw_data) < files_count:
                    print(len(raw_data))
                    print('processing file {}'.format(entry.name))
                    input_data_analyse = []
                    df = pd.read_csv(folder_with_csv_files + '/' + entry.name
                                     , low_memory=False
                                     , usecols=['ts', 'te', 'td', 'sa', 'da', 'sp', 'dp', 'pr', 'ibyt', 'ra', 'ipkt']
                                     , index_col=None
                                     , sep=',')
                    ############################
                    entries_number = df.shape[0] - 3
                    input_data_analyse.append(entries_number)
                    no_zero_td_entries_number = df[~df.td.isin(['0.000'])].shape[0] - 1
                    input_data_analyse.append(no_zero_td_entries_number)
                    bytes_per_5_min = df['ibyt'].sum()
                    input_data_analyse.append(bytes_per_5_min)
                    packets_per_5_min = df['ipkt'].sum()
                    input_data_analyse.append(packets_per_5_min)
                    routers = count_frequency(df['ra'].to_list())
                    input_data_analyse.append(routers)
                    ############################
                    # Prepare input for summary reports
                    series_summary = df.iloc[-1, :6]
                    dict_summary = dict(series_summary)
                    file_name = str(entry.name)
                    date = str(entry.name).split('.')[1]
                    ############################
                    # Get bytes per protocols dictionary
                    protocols_df = df.groupby(['pr'], as_index=False)['ibyt'].sum()
                    protocols_df.set_index('pr', inplace=True)
                    protocols = protocols_df.to_dict('index')
                    ############################
                    # Prepare input for ports reports - ephemeral ports excluded, connection with td=0 excluded
                    df = df[~df.dp.isin(['0', '21548'])]
                    df = df[~df.td.isin(['0.000'])]
                    df = df.loc[df.dp < 49152.0]
                    ports_df = df.groupby(['dp'], as_index=False)['sa'].count().sort_values(by='sa', ascending=False)
                    ports_df = ports_df.iloc[0:NUMBER_OF_PORTS]
                    ports_df.set_index('dp', inplace=True)
                    ports_df = ports_df.to_dict('index')
                    ############################
                    raw_data[date] = [file_name, dict_summary, protocols, ports_df, input_data_analyse]
            except FileNotFoundError:
                print('get_Data(): check path to file or file name')
                sys.exit()
    return raw_data


def count_frequency(list_data):
    freq = dict()
    for item in list_data:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    if np.NAN in freq:
        freq.pop(np.NAN)
    return freq


def get_summary_input_data(data):
    sum_entries_number = 0
    sum_no_zero_td_entries_number = 0
    sum_bytes = 0
    sum_packets = 0
    flows_per_router = dict()
    for k, v in data.items():
        sum_input_data = v[4]
        print(v[4])
        sum_entries_number += sum_input_data[0]
        sum_no_zero_td_entries_number += sum_input_data[1]
        sum_bytes += sum_input_data[2]
        sum_packets += sum_input_data[3]
        for router, flows in sum_input_data[4].items():
            if router not in flows_per_router:
                flows_per_router[router] = flows
            else:
                flows_per_router[router] = flows_per_router[router] + flows
    sort_flows_per_router = sorted(flows_per_router.items(), key=lambda x: x[1], reverse=True)
    out_data = [sum_entries_number,
                sum_no_zero_td_entries_number,
                round(sum_bytes / math.pow(10, 12), 3),
                sum_packets,
                sort_flows_per_router
                ]
    print(out_data)
    return out_data


def get_destination_ports_df(data):
    ports_df = pd.DataFrame()
    for k, v in data.items():
        df = pd.DataFrame.from_dict(v[3])
        ports_df = pd.concat([ports_df, df]).groupby(level=0).sum()
    ports_df = ports_df.T
    ports_df.sort_values(by='sa', inplace=True, ascending=False)
    ports_df = ports_df.iloc[0:NUMBER_OF_PORTS]
    ports_df = ports_df.T
    return ports_df


def get_bytes_per_protocols_df(data):
    bpp_df = pd.DataFrame()
    for k, v in data.items():
        df = pd.DataFrame.from_dict(v[2])
        bpp_df = pd.concat([bpp_df, df]).groupby(level=0).sum()
    return bpp_df


def get_summary_df(data):
    summary_df = pd.DataFrame()
    for k, v in data.items():
        time = dt.strptime(k, '%Y%m%d%H%M')
        df = pd.DataFrame(v[1], index=[time])
        summary_df = pd.concat([summary_df, df])
    summary_df = summary_df.sort_index()
    return summary_df


if __name__ == '__main__':
    input_data = get_data(files_count=288)
    sum_input_data = get_summary_input_data(input_data)
    destination_ports_chart(get_destination_ports_df(input_data))
    protocols = get_bytes_per_protocols_df(input_data)
    bytes_per_L4_protocol_chart(protocols)
    for summary in SUMMARY_OPTIONS:
        get_summary_chart(get_summary_df(input_data), option=summary)
    generate_pdf_file(sum_input_data)
