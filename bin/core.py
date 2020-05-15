import pandas as pd
import os
import sys

from bin.config import INPUT_FILES, PORT_NAME
from bin.pdf_generator import generate_pdf_file
from bin.charts import bar_of_pie_protocols_chart, dest_ports_chart
from bin.charts import bytes_per_L4_protocol_chart


def get_data():
	"""
    functions gets data from fodler ../../netflow_csv, by importing file by file into datafram object
    imported files have to be of csv file type

	:return: tuple with dataframe and files name stored in the folder ../../netflow_csv
	"""
	li = []
	input_files = []
	with os.scandir('../../' + INPUT_FILES) as entries:
		for entry in entries:
			try:
				df = pd.read_csv('../../' + INPUT_FILES + '/' + entry.name, index_col=0, sep=',', low_memory=False)
				print(f'File name: {entry.name}, Rows: {df.shape[0]}')
				li.append(df)
				input_files.append(entry.name)
			except FileNotFoundError:
				print('check path to file or file name')
				sys.exit()
	out = pd.concat(li, axis=0, ignore_index=True)
	return out, input_files


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


def dest_ports(df, get_results=10):
	"""
	:param df: input dataframe
	:param get_results: number of analyzed ports (in descending order in terms of connections number)
	:return: dictionary with port number and number of connections
	"""
	ports = {}
	try:
		df = df[~df.dp.isin(['0','21548'])]
		df = df.loc[df.dp<49152]
		new_df = df.groupby(['dp'], as_index=False)['sa'].count().sort_values(by='sa', ascending=False)[:get_results]
	except KeyError:
		print(f'missing column in input dataframe')
	temp_list = new_df.to_dict(orient='records')
	for item in temp_list:
		new_key = list(item.values())[0]
		new_value = list(item.values())[1]
		ports[new_key] = new_value
	print(ports)
	return ports


if __name__ == '__main__':
	input_data = get_data()
	df = input_data[0]
	dest_ports_chart(dest_ports(df))
	bpp = bytes_per_protocols(df, transport_protocols=True)
	bytes_per_L4_protocol_chart(bpp)
	bpp_all = bytes_per_protocols(df)
	bar_of_pie_protocols_chart(bpp_all)
	generate_pdf_file(input_data[1])
