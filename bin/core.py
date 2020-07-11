import pandas as pd
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
                    df = pd.read_csv(folder_with_csv_files + '/' + entry.name
                                     , low_memory=False
                                     , usecols=['ts', 'te', 'td', 'sa', 'da', 'sp', 'dp', 'pr', 'ibyt']
                                     , index_col=None
                                     , sep=',')
                    # Prepare input for summary reports
                    series_summary = df.iloc[-1, :6]
                    dict_summary = dict(series_summary)
                    file_name = str(entry.name)
                    date = str(entry.name).split('.')[1]
                    # Get bytes per protocols dictionary
                    protocols_df = df.groupby(['pr'], as_index=False)['ibyt'].sum()
                    protocols_df.set_index('pr', inplace=True)
                    protocols = protocols_df.to_dict('index')
                    # Prepare input for ports reports - ephemeral ports excluded, connection with td=0 excluded
                    df = df[~df.dp.isin(['0', '21548'])]
                    df = df[~df.td.isin(['0.000'])]
                    df = df.loc[df.dp < 49152.0]
                    ports_df = df.groupby(['dp'], as_index=False)['sa'].count().sort_values(by='sa', ascending=False)
                    ports_df = ports_df.iloc[0:NUMBER_OF_PORTS]
                    ports_df.set_index('dp', inplace=True)
                    ports_df = ports_df.to_dict('index')
                    raw_data[date] = [file_name, dict_summary, protocols, ports_df]
            except FileNotFoundError:
                print('get_Data(): check path to file or file name')
                sys.exit()
    return raw_data


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


def get_input_file_names(data):
    input_files = []
    for k, v in data.items():
        input_files.append(v[0])
    input_files = sorted(input_files)
    return input_files


if __name__ == '__main__':
    input_data = get_data(files_count=25)
    destination_ports_chart(get_destination_ports_df(input_data))
    protocols = get_bytes_per_protocols_df(input_data)
    bytes_per_L4_protocol_chart(protocols)
    for summary in SUMMARY_OPTIONS:
        get_summary_chart(get_summary_df(input_data), option=summary)
    files = get_input_file_names(input_data)
    generate_pdf_file(files)

